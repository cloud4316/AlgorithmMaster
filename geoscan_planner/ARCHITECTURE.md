# Архитектура Geoscan UAV Planner

## Обзор

Сервис состоит из Python-бэкенда (FastAPI) и браузерного фронтенда (Vanilla JS + Leaflet). Бэкенд обслуживает как REST API, так и статику фронтенда.

```
┌─────────────────────────────────────────────────────────────┐
│                     Браузер (клиент)                        │
│                                                             │
│  ┌─────────────┐          ┌──────────────────────────────┐  │
│  │  Sidebar    │  events  │        Leaflet Map           │  │
│  │  (app.js)   │◄────────►│  OSM tiles + drawn layers   │  │
│  │             │          │  Routes / NFZ / Sites        │  │
│  │  Panels:    │          └──────────────────────────────┘  │
│  │  1. Зоны    │                                            │
│  │  2. Парк    │  fetch /api/plan                          │
│  │  3. Параметры├──────────────────────────────────────►    │
│  │  4. Результаты◄─────────────────────────────────────    │
│  └─────────────┘                                            │
└──────────────────────────────────────┬──────────────────────┘
                                       │ HTTP (port 8001)
┌──────────────────────────────────────▼──────────────────────┐
│                    FastAPI (main.py)                         │
│                                                             │
│  GET /api/uavs      ─── uav_specs.py (UAV_FLEET)           │
│  GET /api/payloads  ─── uav_specs.py (PAYLOAD_SPECS)       │
│                                                             │
│  POST /api/plan ──┐                                         │
│  POST /api/export/kml    ├── optimizer.py → coverage.py     │
│  POST /api/export/geojson┘         │                        │
│                                    ▼                        │
│                             export.py                       │
│                      (KML via simplekml,                    │
│                       GeoJSON native)                       │
└─────────────────────────────────────────────────────────────┘
```

## Модули бэкенда

### `main.py` — FastAPI приложение
- Валидация входных данных (Pydantic models)
- Сборка ответа: запускает `allocate_missions()` дважды при `optimization=both`
- Формирует `summary` с метриками покрытия и оценкой стоимости
- Раздаёт статику фронтенда через `StaticFiles`

### `optimizer.py` — Распределение задач
- `allocate_missions()` — главная точка входа
- **min_time**: делит зону пропорционально ёмкости UAV (скорость × ресурс)
- **min_wear**: делит пропорционально скорости, затем назначает ближайший подполигон
- `_split_proportional()` — нарезка полигона горизонтальными полосами в XY-проекции
- `_assign_nearest()` — жадное / полный перебор (n≤8) назначение ближайшего
- Высотное разделение: UAV_i получает `base_alt + i×10 м`

### `coverage.py` — Генерация маршрута
- `compute_coverage_strips()` — boustrophedon (косилочный) маршрут
  1. Преобразование в XY (equirectangular)
  2. Поворот полигона на `strip_angle` (перпендикулярно ветру)
  3. Вычет бесполётных зон и границы ВП (Shapely)
  4. Генерация параллельных полос с шагом `swath_width`
  5. Расстановка точек фотосъёмки с интервалом `photo_interval`
  6. Обратный поворот координат
- `estimate_stats()` — расчёт расстояния и времени с учётом ветра
- `swath_width()`, `photo_interval()` — расчёт параметров из характеристик камеры

### `uav_specs.py` — Справочники
- `UAV_FLEET`: Geoscan 201, Geoscan Gemini, Geoscan 801
- `PAYLOAD_SPECS`: RGB, Multispectral, IR, LiDAR, Geophysical
- Каждый `UAVSpec` содержит: тип, скорость, ресурс, ветер, высота, нагрузки, взлёт/посадка

### `export.py` — Экспорт
- `missions_to_kml()` — маршруты и точки в KML (simplekml, altitudeMode=relativeToGround)
- `missions_to_geojson()` — маршруты + точки + подполигоны + точки съёмки

## Фронтенд (app.js)

```
state { areaPolygon, airspaceBoundary, nfzPolygons,
        siteMarkers, reserveMarkers, uavRows,
        routeLayers, photoGroup, lastResult, ... }
         │
         ├─ init() ──── /api/uavs, /api/payloads
         ├─ bindEvents() ── кнопки, импорт, экспорт, сценарий
         ├─ map events (Draw.CREATED, click)
         │
         ├─ btn-plan ──► POST /api/plan
         │               │
         │         renderComparison()  ← SVG bar chart
         │         renderMissions()    ← routeGroup + photoGroup
         │         renderSummary()     ← mission cards
         │
         ├─ exportPlan(fmt, opt) ──► POST /api/export/{fmt}
         ├─ saveScenario() ──► download scenario.json
         ├─ loadScenario(file) ──► restore map + params
         └─ importGeoJSON(file) ──► restore zones from GeoJSON
```

## Формула расчёта полос

```
swath_w   = (sensor_w_mm / focal_mm) × altitude_m × (1 − overlap_side)
photo_int = (sensor_h_mm / focal_mm) × altitude_m × (1 − overlap_front)
GSD_cm    = ((sensor_h/focal×alt/4000) + (sensor_w/focal×alt/6000)) / 2 × 100
strip_angle = (wind_dir_deg + 90) % 180
```

## Форматы данных

**GeoJSON (feature_type)**:
- `route` — LineString маршрута навигации
- `photo_line` — MultiPoint точек съёмки (отображается отдельным слоем)
- `sub_polygon` — Polygon подзоны БПЛА
- точки: `action ∈ {takeoff, land, rtl}`

**Сценарий (scenario.json)**:
```json
{"version":2,"params":{...},"area_polygon":[[lat,lon]],"airspace_boundary":null,
 "no_fly_zones":[],"landing_sites":[{"id":"site_1","latlon":[lat,lon]}],
 "reserve_landing_areas":[],"uavs":[{"typeId":"geoscan_201","siteId":"site_1"}]}
```
