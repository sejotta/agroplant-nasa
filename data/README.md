# Extractor de datos climáticos

`clima_json_microclimas.py` descarga datos diarios de [NASA POWER](https://power.larc.nasa.gov/) para una rejilla de puntos dentro de un área, los resume por punto y genera un JSON con las variables de microclima que usamos para construir los escenarios de AGROPLANT.

## Requisitos

- Python 3.9 o superior
- [`requests`](https://pypi.org/project/requests/)

```bash
pip install requests
```

## Uso

```bash
python clima_json_microclimas.py \
  --start 20200101 \
  --end 20201231 \
  --bbox 34,16,56,32.5 \
  --step 2 \
  --out clima_microclimas.json
```

- `--bbox`: `lon_min,lat_min,lon_max,lat_max`. El valor por defecto es una aproximación de Arabia Saudí.
- `--step`: separación entre puntos de la rejilla, en grados. Cuanto más pequeño, más puntos y más peticiones a la API.
- `--community`: `AG` (agricultura), `RE` (energía renovable) o `SB` (edificios). Por defecto, `AG`.

## Qué genera

Un JSON con la fuente, los parámetros, el área y la lista de puntos. Para cada punto:

| Campo | Contenido |
| --- | --- |
| `stats` | Precipitación anual, temperatura media, humedad relativa media y radiación solar media. |
| `microclimate` | Etiqueta (`desert`, `semiarid`, `temperate`), humedad normalizada, exposición solar e índice de sequía. |
| `series` | Serie diaria con fecha, temperatura, precipitación, humedad y radiación. |

## Fuente

- [NASA POWER — API temporal/daily](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)
- [NASA POWER — parámetros](https://power.larc.nasa.gov/docs/tutorials/parameters/)

Los escenarios de AGROPLANT también se apoyaron en datos de [NASA AppEEARS](https://appeears.earthdatacloud.nasa.gov/) para caracterizar distintos ecosistemas.

---

El código de este extractor se distribuye bajo la [licencia MIT](../LICENSE).
