# Climate data extractor

`clima_json_microclimas.py` downloads daily data from [NASA POWER](https://power.larc.nasa.gov/) for a grid of points within an area, summarizes it per point and produces a JSON file with the microclimate variables used to build AGROPLANT's scenarios.

## Requirements

- Python 3.9 or later
- [`requests`](https://pypi.org/project/requests/)

```bash
pip install requests
```

## Usage

```bash
python clima_json_microclimas.py \
  --start 20200101 \
  --end 20201231 \
  --bbox 34,16,56,32.5 \
  --step 2 \
  --out clima_microclimas.json
```

- `--bbox`: `lon_min,lat_min,lon_max,lat_max`. The default is an approximation of Saudi Arabia.
- `--step`: spacing between grid points, in degrees. Smaller values mean more points and more API requests.
- `--community`: `AG` (agriculture), `RE` (renewable energy) or `SB` (buildings). Defaults to `AG`.

## Output

A JSON file with the source, parameters, area and list of points. For each point:

| Field | Contents |
| --- | --- |
| `stats` | Annual precipitation, mean temperature, mean relative humidity and mean solar radiation. |
| `microclimate` | Label (`desert`, `semiarid`, `temperate`), normalized humidity, solar exposure and drought index. |
| `series` | Daily series with date, temperature, precipitation, humidity and radiation. |

## Source

- [NASA POWER — temporal/daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)
- [NASA POWER — parameters](https://power.larc.nasa.gov/docs/tutorials/parameters/)

The AGROPLANT scenarios also drew on [NASA AppEEARS](https://appeears.earthdatacloud.nasa.gov/) data to characterize different ecosystems.

---

The code in this extractor is released under the [MIT license](../LICENSE).
