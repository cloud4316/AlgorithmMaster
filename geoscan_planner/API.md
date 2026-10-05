# API Reference — Geoscan UAV Planner

Base URL: `http://localhost:8001`

---

## GET /api/uavs

Список доступных типов БПЛА.

**Ответ** `200 OK`:
```json
[
  {
    "id": "geoscan_201",
    "name": "Geoscan 201",
    "type": "fixed_wing",
    "max_flight_time_min": 180,
    "cruise_speed_ms": 25,
    "max_wind_ms": 12,
    "max_altitude_agl_m": 3000,
    "supported_payloads": ["rgb","multispectral","ir","lidar","geophysical"],
    "takeoff_type": "catapult",
    "landing_type": "parachute"
  }
]
```

---

## GET /api/payloads

Справочник съёмочных нагрузок.

**Ответ** `200 OK`:
```json
{
  "rgb": {
    "name": "RGB (видимый диапазон)",
    "camera": "Sony RX1R II",
    "resolution_mp": 42.4,
    "focal_mm": 35,
    "sensor_mm": "35.9×24.0 мм",
    "bands": "RGB, 3 канала",
    "gsd_150m_cm": 2.1,
    "notes": "Цифровая модель рельефа + ортофотоплан"
  }
}
```

---

## POST /api/plan

Рассчитать полётные маршруты.

**Тело запроса**:
```json
{
  "area_polygon": [[55.86, 38.02], [55.86, 38.08], [55.90, 38.08], [55.90, 38.02]],
  "no_fly_zones": [
    [[55.87, 38.03], [55.87, 38.05], [55.88, 38.05], [55.88, 38.03]]
  ],
  "airspace_boundary": null,
  "landing_sites": [
    {"id": "site_1", "latlon": [55.868, 38.022], "name": "ВПП Монино"}
  ],
  "reserve_landing_areas": [[55.892, 38.05]],
  "uavs": [
    {"uav_type_id": "geoscan_201", "site_id": "site_1"},
    {"uav_type_id": "geoscan_gemini", "site_id": "site_1"}
  ],
  "payload_type": "rgb",
  "altitude_m": 150,
  "overlap_side": 0.3,
  "overlap_front": 0.7,
  "wind_speed_ms": 3.0,
  "wind_dir_deg": 270,
  "optimization": "both"
}
```

| Поле | Тип | Описание |
|---|---|---|
| `area_polygon` | `[[lat,lon]]` | Зона съёмки, ≥3 точек |
| `no_fly_zones` | `[[[lat,lon]]]` | Бесполётные зоны (необязательно) |
| `airspace_boundary` | `[[lat,lon]]` или `null` | Граница разрешённого ВП |
| `landing_sites` | массив | Предопределённые ВПП |
| `reserve_landing_areas` | `[[lat,lon]]` | Резервные площадки |
| `uavs` | массив | Список БПЛА; указывается `site_id` или `start_latlon` |
| `payload_type` | строка | `rgb` / `multispectral` / `ir` / `lidar` / `geophysical` |
| `altitude_m` | число | Высота AGL, м (базовая; при n>1 БПЛА каждый получает +10 м) |
| `overlap_side` | 0..0.9 | Боковое перекрытие снимков |
| `overlap_front` | 0..0.95 | Продольное перекрытие снимков |
| `wind_speed_ms` | число | Скорость ветра, м/с |
| `wind_dir_deg` | 0..359 | Направление ветра, °(от куда дует) |
| `optimization` | строка | `min_time` / `min_wear` / `both` |

**Ответ** `200 OK` (при `optimization=both`):
```json
{
  "missions": [...],
  "geojson": {...},
  "summary": {
    "total_uavs": 2,
    "max_mission_time_min": 42.3,
    "total_distance_km": 187.4,
    "total_area_km2": 12.1,
    "total_photos": 840,
    "missions": [
      {
        "uav": "Geoscan 201",
        "distance_km": 112.5,
        "time_min": 42.3,
        "altitude_m": 150,
        "area_km2": 7.2,
        "gsd_cm": 2.1,
        "strip_count": 18,
        "photo_count": 504,
        "swath_m": 398.6,
        "cost_rub_est": 10575,
        "takeoff_type": "catapult",
        "landing_type": "parachute"
      }
    ]
  },
  "missions_min_time": [...],
  "missions_min_flight": [...],
  "geojson_min_time": {...},
  "geojson_min_flight": {...},
  "comparison": {
    "min_time": {"max_mission_time_min": 42.3, "total_distance_km": 187.4, "total_flight_hours": 1.75},
    "min_wear": {"max_mission_time_min": 51.0, "total_distance_km": 162.1, "total_flight_hours": 1.41}
  }
}
```

**Поля waypoint**:
```json
{"lat": 55.868, "lon": 38.022, "alt_m": 150, "action": "photo", "strip_id": 3, "phase": "SURVEY"}
```

Значения `action`: `takeoff`, `survey_start`, `photo`, `survey_end`, `rtl`, `land`  
Значения `phase`: `TAKEOFF`, `SURVEY_START`, `SURVEY`, `SURVEY_END`, `RTL`, `LAND`, `CRUISE`

---

## POST /api/export/kml

Экспорт в KML (Google Earth / Mission Planner).

Тело запроса — то же что `/api/plan`.  
Ответ: `application/vnd.google-earth.kml+xml`, файл `flight_plan.kml`.

```bash
curl -X POST http://localhost:8001/api/export/kml \
  -H 'Content-Type: application/json' \
  -d '{"area_polygon":[[55.86,38.02],[55.86,38.08],[55.90,38.08],[55.90,38.02]],"uavs":[{"uav_type_id":"geoscan_201","start_latlon":[55.86,38.02]}],"optimization":"min_time"}' \
  -o flight_plan.kml
```

---

## POST /api/export/geojson

Экспорт в GeoJSON (QGIS, любой ГИС-инструмент).

Тело запроса — то же что `/api/plan`.  
Ответ: `application/geo+json`, файл `flight_plan.geojson`.

```bash
curl -X POST http://localhost:8001/api/export/geojson \
  -H 'Content-Type: application/json' \
  -d '{"area_polygon":[[55.86,38.02],[55.86,38.08],[55.90,38.08],[55.90,38.02]],"uavs":[{"uav_type_id":"geoscan_gemini","start_latlon":[55.86,38.02]}],"optimization":"min_wear"}' \
  -o flight_plan.geojson
```

---

## Коды ошибок

| Код | Причина |
|---|---|
| `400` | Неизвестный тип БПЛА / нагрузки; превышен ветер / высота; не задан старт |
| `422` | Ошибка валидации входного JSON (Pydantic) |
| `500` | Внутренняя ошибка геометрических вычислений |
