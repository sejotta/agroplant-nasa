#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descarga clima diario (NASA POWER) en JSON para un AOI (rejilla de puntos),
resume por punto y genera etiquetas/pares microclimáticos simples.

Fuentes (API oficial):
- Overview y servicios: https://power.larc.nasa.gov/docs/services/api/
- Daily point: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- Parámetros: https://power.larc.nasa.gov/docs/tutorials/parameters/
- Monthly/Annual, Hourly (si los necesitas): ver docs temporales.
"""
import argparse, json, math, time
from datetime import datetime
from typing import Dict, Any, List, Tuple

import requests

API = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMS = ["T2M","T2M_MAX","T2M_MIN","PRECTOTCORR","RH2M","ALLSKY_SFC_SW_DWN"]  # °C, mm/día, %, MJ/m²/día

def build_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept":"application/json","User-Agent":"clima-json-microclimas/1.0"})
    return s

def fetch_point_daily(session: requests.Session, lat: float, lon: float, start: str, end: str,
                      community: str="AG", max_retries: int=4) -> Dict[str, Any]:
    """
    Llama a POWER daily/point. start/end formato AAAAMMDD.
    Reintenta con backoff si 429/5xx.
    """
    url = (f"{API}?parameters={','.join(PARAMS)}&start={start}&end={end}"
           f"&latitude={lat}&longitude={lon}&community={community}&format=JSON")
    delay = 1.0
    for i in range(max_retries):
        r = session.get(url, timeout=60)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429,500,502,503,504):
            time.sleep(delay); delay = min(delay*2, 30)
            continue
        r.raise_for_status()
    raise RuntimeError(f"Fallo tras reintentos: {url}")

def daily_json_to_timeseries(js: Dict[str, Any]) -> List[Dict[str, Any]]:
    """POWER devuelve properties.parameter.{PARAM}[date->value]. Normaliza a lista por fecha."""
    param = js["properties"]["parameter"]
    # Fechas están en las claves del primer parámetro
    any_series = next(iter(param.values()))
    dates = sorted(any_series.keys())
    out = []
    for d in dates:
        row = {"date": f"{d[:4]}-{d[4:6]}-{d[6:]}"}  # YYYY-MM-DD
        for p in PARAMS:
            v = param.get(p, {}).get(d, None)
            # POWER entrega °C ya en T2M; precip en mm/día; RH en %; SW en MJ/m²/día
            key_map = {
                "T2M":"t2m_c", "T2M_MAX":"t2m_max_c", "T2M_MIN":"t2m_min_c",
                "PRECTOTCORR":"precip_mm", "RH2M":"rh2m_pct",
                "ALLSKY_SFC_SW_DWN":"sw_down_mj"
            }
            row[key_map[p]] = v
        out.append(row)
    return out

def summarize_point(series: List[Dict[str, Any]]) -> Dict[str, float]:
    """Agrega anual por punto."""
    if not series:
        return {}
    n = len(series)
    s_prec = sum(x["precip_mm"] for x in series if x["precip_mm"] is not None)
    mean_t2m = sum(x["t2m_c"] for x in series if x["t2m_c"] is not None) / n
    mean_rh = sum(x["rh2m_pct"] for x in series if x["rh2m_pct"] is not None) / n
    mean_sw = sum(x["sw_down_mj"] for x in series if x["sw_down_mj"] is not None) / n
    return {
        "annual_precip_mm": round(s_prec, 2),
        "mean_t2m_c": round(mean_t2m, 2),
        "mean_rh2m_pct": round(mean_rh, 2),
        "mean_sw_down_mj_per_m2_day": round(mean_sw, 2),
        "n_days": n
    }

def microclimate_from_stats(stats: Dict[str, float]) -> Dict[str, Any]:
    """Reglas simples y continuas para IA downstream."""
    p = stats["annual_precip_mm"]
    rh = stats["mean_rh2m_pct"]
    sw = stats["mean_sw_down_mj_per_m2_day"]

    if p < 250:
        label = "desert"
    elif p < 500:
        label = "semiarid"
    else:
        label = "temperate"

    humidity_level = max(0.0, min(rh/100.0, 1.0))
    solar_exposure = max(0.0, min(sw/30.0, 1.0))   # 30 MJ/m²/día ~ alto
    drought_index = 1.0 - min(p/500.0, 1.0)        # 1 = más sequía

    return {
        "label": label,
        "humidity_level": round(humidity_level, 3),
        "solar_exposure": round(solar_exposure, 3),
        "drought_index": round(drought_index, 3)
    }

def make_grid(bbox: Tuple[float,float,float,float], step_deg: float) -> List[Tuple[float,float]]:
    """Devuelve lista (lat, lon) en rejilla regular dentro del bbox."""
    lon_min, lat_min, lon_max, lat_max = bbox
    pts = []
    lat = lat_min
    while lat <= lat_max + 1e-9:
        lon = lon_min
        while lon <= lon_max + 1e-9:
            pts.append((round(lat,6), round(lon,6)))
            lon += step_deg
        lat += step_deg
    return pts

def main():
    ap = argparse.ArgumentParser(description="POWER -> JSON con microclimas simples")
    ap.add_argument("--start", default="20200101", help="AAAAMMDD")
    ap.add_argument("--end",   default="20201231", help="AAAAMMDD")
    # BBox Arabia Saudita aprox: lon_min, lat_min, lon_max, lat_max
    ap.add_argument("--bbox",  default="34,16,56,32.5",
                    help="lon_min,lat_min,lon_max,lat_max")
    ap.add_argument("--step",  type=float, default=1.0, help="grados de rejilla (puntos)")
    ap.add_argument("--community", default="AG", choices=["AG","RE","SB"], help="comunidad POWER")
    ap.add_argument("--out",   default="clima_microclimas.json")
    args = ap.parse_args()

    bbox = tuple(float(x) for x in args.bbox.split(","))
    pts = make_grid(bbox, args.step)

    s = build_session()
    out_points = []
    for i, (lat, lon) in enumerate(pts, start=1):
        js = fetch_point_daily(s, lat, lon, args.start, args.end, args.community)
        series = daily_json_to_timeseries(js)
        stats = summarize_point(series)
        micro = microclimate_from_stats(stats)
        out_points.append({
            "id": f"pt-{i}",
            "lat": lat, "lon": lon,
            "stats": stats,
            "microclimate": micro,
            "series": series
        })

    out = {
        "source": "NASA POWER temporal/daily/point",
        "parameters": PARAMS,
        "community": args.community,
        "bbox": {"lon_min": bbox[0], "lat_min": bbox[1], "lon_max": bbox[2], "lat_max": bbox[3]},
        "grid_step_deg": args.step,
        "start": args.start, "end": args.end,
        "points": out_points,
        "generated_utc": datetime.utcnow().isoformat(timespec="seconds")+"Z"
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"OK -> {args.out}  pts={len(out_points)}")

if __name__ == "__main__":
    main()