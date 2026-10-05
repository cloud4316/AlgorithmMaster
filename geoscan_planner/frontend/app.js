'use strict';

const API = '';

// ─── State ───────────────────────────────────────────────────────────────────
const state = {
  areaPolygon: null,     // legacy ref to last area polygon (single-zone)
  areaPolygons: [],      // all area polygon layers (multi-zone)
  airspaceBoundary: null,
  nfzPolygons: [],
  siteMarkers: [],
  reserveMarkers: [],
  gcpMarkers: [],
  uavRows: [],
  routeLayers: [],
  rangeRings: [],
  photoGroup: null,
  uavTypes: [],
  payloadSpecs: {},
  lastMissions: null,
  lastResult: null,
  lastRequest: null,
  settingStartFor: null,
  addingReserve: false,
  addingSite: false,
  activeOpt: 'min_time',
};

// ─── Map ─────────────────────────────────────────────────────────────────────
const map = L.map('map', { center: [55.75, 37.62], zoom: 11 });

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors', maxZoom: 19,
}).addTo(map);

const drawnItems = new L.FeatureGroup().addTo(map);
const drawControl = new L.Control.Draw({
  draw: {
    polygon: { shapeOptions: { color: '#3b82f6', fillOpacity: 0.15 } },
    rectangle: { shapeOptions: { color: '#3b82f6', fillOpacity: 0.15 } },
    polyline: false, circle: false, circlemarker: false, marker: false,
  },
  edit: { featureGroup: drawnItems },
});
map.addControl(drawControl);

// ─── Wind indicator control ───────────────────────────────────────────────────
const WindControl = L.Control.extend({
  options: { position: 'bottomright' },
  onAdd() {
    this._div = L.DomUtil.create('div', 'wind-indicator');
    this._div.title = 'Ветер: скорость и направление';
    this.update(0, 0);
    return this._div;
  },
  update(speed, dir) {
    const calm = speed < 0.5;
    const arrowRot = dir;
    this._div.innerHTML = `
      <svg width="52" height="52" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
        <circle cx="26" cy="26" r="24" fill="rgba(15,23,42,0.75)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
        <text x="26" y="15" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.5)" font-family="sans-serif">С</text>
        <text x="26" y="43" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.5)" font-family="sans-serif">Ю</text>
        <text x="7"  y="29" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.5)" font-family="sans-serif">З</text>
        <text x="45" y="29" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.5)" font-family="sans-serif">В</text>
        ${calm ? '' : `<g transform="translate(26,26) rotate(${arrowRot})">
          <polygon points="0,-13 4,2 0,-1 -4,2" fill="${speed > 10 ? '#ef4444' : speed > 5 ? '#f59e0b' : '#3b82f6'}"/>
        </g>`}
        <text x="26" y="30" text-anchor="middle" font-size="8.5" font-weight="700" fill="white" font-family="sans-serif">${calm ? '—' : speed.toFixed(1)}</text>
        <text x="26" y="39" text-anchor="middle" font-size="6" fill="rgba(255,255,255,0.6)" font-family="sans-serif">${calm ? 'штиль' : 'м/с'}</text>
      </svg>`;
  }
});
const windControl = new WindControl();
windControl.addTo(map);

function updateWindControl() {
  const s = +document.getElementById('wind-speed').value || 0;
  const d = +document.getElementById('wind-dir').value || 0;
  windControl.update(s, d);
}
document.getElementById('wind-speed').addEventListener('input', updateWindControl);
document.getElementById('wind-dir').addEventListener('input', updateWindControl);

const ROUTE_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#a855f7'];

const TASK_TEMPLATES = {
  agriculture:    { altitude_m: 100, overlap_side: 30, overlap_front: 80, payload_type: 'multispectral' },
  mapping:        { altitude_m: 200, overlap_side: 30, overlap_front: 70, payload_type: 'rgb' },
  infrastructure: { altitude_m:  80, overlap_side: 60, overlap_front: 80, payload_type: 'rgb' },
  search:         { altitude_m: 150, overlap_side: 40, overlap_front: 60, payload_type: 'ir' },
  lidar:          { altitude_m: 100, overlap_side: 50, overlap_front: 60, payload_type: 'lidar' },
};

// ─── Init ────────────────────────────────────────────────────────────────────
async function init() {
  [state.uavTypes, state.payloadSpecs] = await Promise.all([
    fetchJSON('/api/uavs'),
    fetchJSON('/api/payloads'),
  ]);
  addUAVRow();
  bindEvents();
  renderPayloadInfo(document.getElementById('payload-type').value);
  renderFleetRef();
  checkAutoRestore();
  checkShareHash();
}

// ─── UAV rows ────────────────────────────────────────────────────────────────
let _uavCounter = 0;

function addUAVRow() {
  const id = ++_uavCounter;
  state.uavRows.push({ id, typeId: state.uavTypes[0]?.id, startLatLon: null, marker: null, siteId: null });
  renderUAVRows();
}

function removeUAVRow(id) {
  const row = state.uavRows.find(r => r.id === id);
  if (row?.marker) map.removeLayer(row.marker);
  state.uavRows = state.uavRows.filter(r => r.id !== id);
  renderUAVRows();
}

function renderUAVRows() {
  const container = document.getElementById('uav-list');
  container.innerHTML = '';
  const hasSites = state.siteMarkers.length > 0;

  state.uavRows.forEach(row => {
    const div = document.createElement('div');
    div.className = 'uav-row';

    const siteOptions = hasSites
      ? state.siteMarkers.map(s =>
          `<option value="${s.id}" ${row.siteId === s.id ? 'selected' : ''}>${s.id} (${s.latlon[0].toFixed(4)}, ${s.latlon[1].toFixed(4)})</option>`
        ).join('')
      : '';

    const spec = state.uavTypes.find(t => t.id === row.typeId) || {};
    const currentPayload = document.getElementById('payload-type')?.value || 'rgb';
    const payloadOk = !spec.id || (spec.supported_payloads || []).includes(currentPayload);
    const specHtml = spec.id ? `
      <div class="uav-mini-spec">
        <span>${spec.type === 'fixed_wing' ? '✈ Самолёт' : '🚁 Мультиротор'}</span>
        <span>${spec.max_flight_time_min} мин</span>
        <span>${Math.round(spec.cruise_speed_ms * 3.6)} км/ч</span>
        <span>${spec.takeoff_type === 'catapult' ? 'Катапульта' : 'ВТОЛ'} / ${spec.landing_type === 'parachute' ? 'Парашют' : 'ВТОЛ'}</span>
        <span>≤${spec.max_wind_ms} м/с ветер</span>
      </div>
      ${!payloadOk ? `<div style="font-size:10px;color:#ef4444;padding:2px 0">⚠ ${spec.name} не поддерживает «${currentPayload}»</div>` : ''}` : '';
    div.innerHTML = `
      <div class="row-controls">
        <select class="uav-type-sel">
          ${state.uavTypes.map(t =>
            `<option value="${t.id}" ${t.id === row.typeId ? 'selected' : ''}>${t.name}</option>`
          ).join('')}
        </select>
        <button class="btn btn-ghost btn-sm remove-uav-btn">✕</button>
      </div>
      ${specHtml}
      ${hasSites ? `
        <label class="site-label">ВПП старта
          <select class="site-sel">
            <option value="">— выбрать ВПП —</option>
            ${siteOptions}
          </select>
        </label>
      ` : `
        <div class="row-controls">
          <button class="btn btn-ghost btn-sm set-start-btn">📍 Задать старт</button>
          <span class="uav-start-info">${row.startLatLon
            ? `${row.startLatLon[0].toFixed(5)}, ${row.startLatLon[1].toFixed(5)}`
            : 'Кликните на карту'}</span>
        </div>
      `}
    `;
    div.querySelector('.uav-type-sel').addEventListener('change', e => { row.typeId = e.target.value; });
    div.querySelector('.remove-uav-btn').addEventListener('click', () => removeUAVRow(row.id));
    if (hasSites) {
      div.querySelector('.site-sel').addEventListener('change', e => { row.siteId = e.target.value || null; });
    } else {
      div.querySelector('.set-start-btn').addEventListener('click', () => {
        state.settingStartFor = row.id;
        state.addingReserve = false;
        state.addingSite = false;
        setStatus('Кликните на карту для точки старта БВС', 'loading');
      });
    }
    container.appendChild(div);
  });
}

// ─── Map click: UAV start or reserve landing ──────────────────────────────────
map.on('click', e => {
  if (state.addingSite) {
    const siteId = `site_${state.siteMarkers.length + 1}`;
    const m = L.marker(e.latlng, {
      icon: L.divIcon({
        className: '',
        html: `<div style="background:#22c55e;width:16px;height:16px;
                    border-radius:3px;border:2px solid #fff;display:flex;align-items:center;
                    justify-content:center;font-size:9px;font-weight:700;color:#000">${state.siteMarkers.length + 1}</div>`,
        iconSize: [16, 16], iconAnchor: [8, 8],
      }),
    }).addTo(map).bindPopup(`ВПП ${siteId}: ${e.latlng.lat.toFixed(5)}, ${e.latlng.lng.toFixed(5)}`);
    state.siteMarkers.push({ id: siteId, latlon: [e.latlng.lat, e.latlng.lng], marker: m });
    updateAreaInfo();
    renderUAVRows();  // refresh site dropdowns
    setStatus(`ВПП ${siteId} добавлен (всего: ${state.siteMarkers.length})`, 'ok');
    return;
  }

  if (state.addingReserve) {
    const m = L.marker(e.latlng, {
      icon: L.divIcon({
        className: '',
        html: `<div style="background:#f59e0b;width:14px;height:14px;
                    border-radius:3px;border:2px solid #fff;transform:rotate(45deg)"></div>`,
        iconSize: [14, 14], iconAnchor: [7, 7],
      }),
    }).addTo(map).bindPopup(`Резервная площадка: ${e.latlng.lat.toFixed(5)}, ${e.latlng.lng.toFixed(5)}`);
    state.reserveMarkers.push(m);
    updateAreaInfo();
    setStatus(`Резервная площадка добавлена (${state.reserveMarkers.length} шт.)`, 'ok');
    return;
  }

  if (state.settingStartFor == null) return;
  const row = state.uavRows.find(r => r.id === state.settingStartFor);
  if (!row) return;

  row.startLatLon = [e.latlng.lat, e.latlng.lng];
  if (row.marker) map.removeLayer(row.marker);
  row.marker = L.marker(e.latlng, {
    icon: L.divIcon({
      className: '',
      html: `<div style="background:${ROUTE_COLORS[(row.id - 1) % ROUTE_COLORS.length]};
                         width:12px;height:12px;border-radius:50%;border:2px solid #fff;"></div>`,
      iconSize: [12, 12], iconAnchor: [6, 6],
    }),
  }).addTo(map).bindPopup(`${row.typeId} — точка старта`);

  state.settingStartFor = null;
  renderUAVRows();
  setStatus('Точка старта задана', 'ok');
});

// ─── Drawing mode flags ───────────────────────────────────────────────────────
let _drawMode = null; // 'area' | 'airspace' | 'nfz'

document.getElementById('btn-draw-area').addEventListener('click', () => {
  _drawMode = 'area';
  state.addingReserve = false;
  const nextColor = ROUTE_COLORS[state.areaPolygons.length % ROUTE_COLORS.length];
  new L.Draw.Polygon(map, { shapeOptions: { color: nextColor, fillOpacity: 0.15 } }).enable();
  setStatus('Нарисуйте зону съёмки', 'loading');
});

document.getElementById('btn-draw-airspace').addEventListener('click', () => {
  _drawMode = 'airspace';
  state.addingReserve = false;
  new L.Draw.Polygon(map, {
    shapeOptions: { color: '#a855f7', fillOpacity: 0.08, dashArray: '8,4' },
  }).enable();
  setStatus('Нарисуйте границу воздушного пространства', 'loading');
});

document.getElementById('btn-draw-nfz').addEventListener('click', () => {
  _drawMode = 'nfz';
  state.addingReserve = false;
  new L.Draw.Polygon(map, {
    shapeOptions: { color: '#ef4444', fillOpacity: 0.2, dashArray: '6,4', className: 'nfz-animated' },
  }).enable();
  setStatus('Нарисуйте бесполётную зону', 'loading');
});

document.getElementById('btn-add-site').addEventListener('click', () => {
  state.addingSite = !state.addingSite;
  state.addingReserve = false;
  state.settingStartFor = null;
  document.getElementById('btn-add-reserve').classList.remove('active');
  if (state.addingSite) {
    document.getElementById('btn-add-site').classList.add('active');
    setStatus('Кликните на карту для добавления взлётно-посадочного пункта (ВПП)', 'loading');
  } else {
    document.getElementById('btn-add-site').classList.remove('active');
    setStatus('');
  }
});

document.getElementById('btn-add-reserve').addEventListener('click', () => {
  state.addingReserve = !state.addingReserve;
  state.addingSite = false;
  state.settingStartFor = null;
  document.getElementById('btn-add-site').classList.remove('active');
  if (state.addingReserve) {
    document.getElementById('btn-add-reserve').classList.add('active');
    setStatus('Кликните на карту для добавления резервной площадки посадки', 'loading');
  } else {
    document.getElementById('btn-add-reserve').classList.remove('active');
    setStatus('');
  }
});

document.getElementById('btn-clear').addEventListener('click', clearAll);

map.on(L.Draw.Event.CREATED, e => {
  const layer = e.layer;
  if (_drawMode === 'airspace') {
    layer.setStyle({ color: '#a855f7', fillOpacity: 0.08, dashArray: '8,4' });
    layer._layerType = 'airspace';
    if (state.airspaceBoundary) drawnItems.removeLayer(state.airspaceBoundary);
    state.airspaceBoundary = layer;
  } else if (_drawMode === 'nfz') {
    layer.setStyle({ color: '#ef4444', fillOpacity: 0.2, dashArray: '6,4' });
    layer._layerType = 'nfz';
    _addNfzBuffer(layer);
  } else {
    // Multiple survey zones: each new draw adds a zone (different color per zone)
    const zoneIdx = state.areaPolygons.length;
    const color = ROUTE_COLORS[zoneIdx % ROUTE_COLORS.length];
    layer.setStyle({ color, fillOpacity: 0.15 });
    layer._layerType = 'area';
    layer._zoneIndex = zoneIdx;
    layer.bindTooltip(`Зона ${zoneIdx + 1}`, { permanent: true, direction: 'center', className: 'zone-label' });
    state.areaPolygons.push(layer);
    state.areaPolygon = layer; // keep legacy ref
  }
  drawnItems.addLayer(layer);
  _drawMode = null;
  updateAreaInfo();
  setStatus('');
});

map.on(L.Draw.Event.DELETED, () => {
  state.areaPolygons = [];
  state.areaPolygon = null;
  state.airspaceBoundary = null;
  drawnItems.eachLayer(l => {
    if (l._layerType === 'area') { state.areaPolygons.push(l); state.areaPolygon = l; }
    if (l._layerType === 'airspace') state.airspaceBoundary = l;
  });
  updateAreaInfo();
});

map.on(L.Draw.Event.EDITED, () => updateAreaInfo());

map.on('draw:drawvertex', e => {
  try {
    const layers = e.layers?.getLayers?.() || [];
    const poly = layers[0];
    if (!poly) return;
    const lls = (poly.getLatLngs()[0] || []);
    if (lls.length < 3) return;
    const area = L.GeometryUtil?.geodesicArea(lls);
    if (area) document.getElementById('area-info').innerHTML =
      `✏️ Текущая зона: <b>${(area / 1e6).toFixed(2)} км²</b> (${lls.length} вершин)`;
  } catch {}
});

function updateAreaInfo() {
  // Update zone tooltips with areas
  state.areaPolygons.forEach((l, i) => {
    try {
      const area = L.GeometryUtil?.geodesicArea(l.getLatLngs()[0]);
      if (area) l.setTooltipContent(`Зона ${i + 1} — ${(area / 1e6).toFixed(2)} км²`);
    } catch {}
  });
  const nfzCount = [...drawnItems.getLayers()].filter(l => l._layerType === 'nfz').length;
  const box = document.getElementById('area-info');
  const parts = [];
  if (state.areaPolygons.length === 1) {
    const pts = state.areaPolygons[0].getLatLngs()[0];
    parts.push(`Зона: ~${roughArea(pts).toFixed(2)} км²`);
  } else if (state.areaPolygons.length > 1) {
    const total = state.areaPolygons.reduce((s, l) => s + roughArea(l.getLatLngs()[0]), 0);
    parts.push(`Зоны: ${state.areaPolygons.length} (~${total.toFixed(2)} км²)`);
  }
  if (state.airspaceBoundary) parts.push('ВП: задано');
  if (nfzCount) parts.push(`БЗ: ${nfzCount}`);
  if (state.siteMarkers.length) parts.push(`ВПП: ${state.siteMarkers.length}`);
  if (state.reserveMarkers.length) parts.push(`Резерв: ${state.reserveMarkers.length}`);
  // UAV count recommendation
  if (state.areaPolygons.length > 0) {
    const totalKm2 = state.areaPolygons.reduce((s, l) => s + roughArea(l.getLatLngs()[0]), 0);
    const alt = +document.getElementById('altitude').value || 150;
    const uavType = state.uavRows[0]?.type || 'geoscan_201';
    const uavSpec = state.uavTypes.find(t => t.id === uavType);
    const speed = uavSpec?.cruise_speed_ms || 25;
    const maxTime = (uavSpec?.max_flight_time_min || 180) * 0.85;
    const sideOvlp = (+document.getElementById('overlap-side').value || 30) / 100;
    const sensorW = uavSpec?.default_sensor_w_mm || 35.9;
    const focal = uavSpec?.default_focal_mm || 35;
    const swath = sensorW / focal * alt;
    const stripSpacing = swath * (1 - sideOvlp);
    const stripLenEst = Math.sqrt(totalKm2) * 1000;
    const stripsPerKm2 = 1000 / stripSpacing;
    const distPerKm2 = stripsPerKm2 * stripLenEst / totalKm2;
    const timePerKm2Min = distPerKm2 / speed / 60;
    const recUAVs = Math.max(1, Math.ceil(totalKm2 * timePerKm2Min / maxTime));
    if (recUAVs > 1) parts.push(`💡 рек. ${recUAVs} БВС`);
    // Live GSD estimate
    const uavSpec2 = state.uavTypes.find(t => t.id === (state.uavRows[0]?.typeId));
    if (uavSpec2) {
      const pSpec = state.payloadSpecs?.[document.getElementById('payload-type')?.value] || {};
      const pixUm = pSpec.pixel_um || 4.51;
      const fMm = uavSpec2.focal_mm || 35;
      const gsdCm = pixUm * alt / fMm / 10;
      parts.push(`GSD≈${gsdCm.toFixed(1)}см`);
    }
  }
  box.innerHTML = parts.join(' | ') || 'Зона не задана';
  box.classList.toggle('has-data', state.areaPolygons.length > 0);
}

function roughArea(latlngs) {
  const R = 6371000;
  let area = 0;
  const n = latlngs.length;
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    area += Math.PI / 180 * (latlngs[j].lng - latlngs[i].lng)
          * (2 + Math.sin(Math.PI / 180 * latlngs[i].lat)
               + Math.sin(Math.PI / 180 * latlngs[j].lat));
  }
  return Math.abs(area * R * R / 2) / 1e6;
}

function clearAll() {
  drawnItems.clearLayers();
  state.areaPolygon = null;
  state.areaPolygons = [];
  state.airspaceBoundary = null;
  state.siteMarkers.forEach(s => map.removeLayer(s.marker));
  state.siteMarkers = [];
  state.reserveMarkers.forEach(m => map.removeLayer(m));
  state.reserveMarkers = [];
  state.gcpMarkers.forEach(m => map.removeLayer(m));
  state.gcpMarkers = [];
  state.routeLayers.forEach(l => map.removeLayer(l));
  state.routeLayers = [];
  (state.rangeRings || []).forEach(l => map.removeLayer(l));
  state.rangeRings = [];
  state.lastMissions = null;
  state.lastResult = null;
  state.addingReserve = false;
  document.getElementById('btn-add-reserve').classList.remove('active');
  document.getElementById('results-panel').style.display = 'none';
  document.getElementById('opt-toggle').style.display = 'none';
  updateAreaInfo();
  setStatus('');
}

function latlngsToArray(latlngs) {
  return latlngs.map(ll => [ll.lat, ll.lng]);
}

function _addNfzBuffer(nfzLayer) {
  const pts = nfzLayer.getLatLngs()[0] || [];
  if (pts.length < 3) return;
  const mPerDeg = 111320;
  const avgLat = pts.reduce((s, p) => s + p.lat, 0) / pts.length;
  const centLon = pts.reduce((s, p) => s + p.lng, 0) / pts.length;
  const bufLat = 80 / mPerDeg;
  const bufLon = 80 / (mPerDeg * Math.cos(avgLat * Math.PI / 180));
  const expanded = pts.map(p => {
    const dlat = p.lat - avgLat, dlng = p.lng - centLon;
    const dist = Math.sqrt((dlat * mPerDeg) ** 2 + (dlng * mPerDeg * Math.cos(avgLat * Math.PI / 180)) ** 2);
    if (dist < 1) return [p.lat + bufLat, p.lng + bufLon];
    const scale = (dist + 80) / dist;
    return [avgLat + dlat * scale, centLon + dlng * scale];
  });
  const bufLayer = L.polygon(expanded, {
    color: '#ef4444', weight: 1, opacity: 0.4, fillColor: '#ef4444', fillOpacity: 0.04,
    dashArray: '4,4',
  });
  bufLayer.bindTooltip('Буфер безопасности 80 м вокруг БЗ', { sticky: true, className: 'nfz-tooltip' });
  bufLayer._layerType = 'nfz-buffer';
  nfzLayer._bufferLayer = bufLayer;
  drawnItems.addLayer(bufLayer);
}

function collectPolygons() {
  const nfzs = [...drawnItems.getLayers()].filter(l => l._layerType === 'nfz');
  return { nfzs };
}

// ─── Plan ────────────────────────────────────────────────────────────────────
document.getElementById('btn-plan').addEventListener('click', async () => {
  if (state.areaPolygons.length === 0) {
    setStatus('Сначала нарисуйте зону съёмки', 'error'); return;
  }
  const { nfzs } = collectPolygons();
  const hasSites = state.siteMarkers.length > 0;

  const badUAVs = state.uavRows.filter(r =>
    hasSites ? !r.siteId : !r.startLatLon
  );
  if (badUAVs.length) {
    setStatus(hasSites ? 'Выберите ВПП для каждого БВС' : 'Задайте точку старта для всех БВС', 'error');
    return;
  }

  // Pre-flight validation
  const alt = +document.getElementById('altitude').value;
  const wind = +document.getElementById('wind-speed').value;
  for (const row of state.uavRows) {
    const spec = state.uavTypes.find(t => t.id === row.typeId);
    if (spec) {
      if (alt > spec.max_altitude_agl_m) {
        setStatus(`${spec.name}: высота ${alt} м > макс. ${spec.max_altitude_agl_m} м`, 'error'); return;
      }
      if (wind > spec.max_wind_ms) {
        setStatus(`${spec.name}: ветер ${wind} м/с > макс. ${spec.max_wind_ms} м/с`, 'error'); return;
      }
      const payload = document.getElementById('payload-type').value;
      if (!(spec.supported_payloads || []).includes(payload)) {
        setStatus(`${spec.name}: не поддерживает «${payload}»`, 'error'); return;
      }
    }
  }

  const activeZones = state.areaPolygons.map(l => latlngsToArray(l.getLatLngs()[0]));

  const body = {
    area_polygons: activeZones,
    no_fly_zones: nfzs.map(n => latlngsToArray(n.getLatLngs()[0])),
    airspace_boundary: state.airspaceBoundary
      ? latlngsToArray(state.airspaceBoundary.getLatLngs()[0]) : null,
    landing_sites: state.siteMarkers.map(s => ({ id: s.id, latlon: s.latlon, name: s.id })),
    reserve_landing_areas: state.reserveMarkers.map(m => [m.getLatLng().lat, m.getLatLng().lng]),
    uavs: state.uavRows.map(r => hasSites
      ? { uav_type_id: r.typeId, site_id: r.siteId }
      : { uav_type_id: r.typeId, start_latlon: r.startLatLon, land_latlon: r.startLatLon }
    ),
    payload_type: document.getElementById('payload-type').value,
    altitude_m: +document.getElementById('altitude').value,
    overlap_side: +document.getElementById('overlap-side').value / 100,
    overlap_front: +document.getElementById('overlap-front').value / 100,
    wind_speed_ms: +document.getElementById('wind-speed').value,
    wind_dir_deg: +document.getElementById('wind-dir').value,
    optimization: document.getElementById('optimization').value,
    startup_cost_min: +document.getElementById('startup-cost').value,
  };

  state.lastRequest = body;
  state._planAbortController?.abort();
  state._planAbortController = new AbortController();
  setStatus('Вычисление маршрутов…', 'loading');

  try {
    const result = await fetchJSON('/api/plan', 'POST', body, state._planAbortController.signal);
    state.lastResult = result;

    if (result.comparison) {
      // Both optimizations — show comparison and toggle
      renderComparison(result.comparison);
      state.activeOpt = 'min_time';
      renderMissions(result.missions_min_time, result.geojson_min_time, result.summary);
      document.getElementById('opt-toggle').style.display = 'flex';
      document.getElementById('btn-show-min-time').classList.add('active-opt');
      document.getElementById('btn-show-min-wear').classList.remove('active-opt');
      document.getElementById('export-row-single').style.display = 'none';
      document.getElementById('export-row-both').style.display = '';
    } else {
      document.getElementById('results-comparison').innerHTML = '';
      document.getElementById('opt-toggle').style.display = 'none';
      renderMissions(result.missions, result.geojson, result.summary);
      document.getElementById('export-row-single').style.display = '';
      document.getElementById('export-row-both').style.display = 'none';
    }

    setStatus(`Готово: ${result.summary.total_uavs} БВС, ${result.summary.total_distance_km.toFixed(1)} км`, 'ok');
    autoSaveScenario();
  } catch (err) {
    if (err.name === 'AbortError') return;
    setStatus('Ошибка: ' + err.message, 'error');
  }
});

// ─── Optimization toggle ──────────────────────────────────────────────────────
document.getElementById('btn-show-min-time').addEventListener('click', () => {
  if (!state.lastResult?.missions_min_time) return;
  state.activeOpt = 'min_time';
  renderMissions(state.lastResult.missions_min_time, state.lastResult.geojson_min_time, state.lastResult.summary);
  document.getElementById('btn-show-min-time').classList.add('active-opt');
  document.getElementById('btn-show-min-wear').classList.remove('active-opt');
});

document.getElementById('btn-show-min-wear').addEventListener('click', () => {
  if (!state.lastResult?.missions_min_flight) return;
  state.activeOpt = 'min_wear';
  const s = _make_summary_from_missions(state.lastResult.missions_min_flight, 'min_wear');
  renderMissions(state.lastResult.missions_min_flight, state.lastResult.geojson_min_flight, s);
  document.getElementById('btn-show-min-wear').classList.add('active-opt');
  document.getElementById('btn-show-min-time').classList.remove('active-opt');
});

function _make_summary_from_missions(missions, opt) {
  return {
    total_uavs: missions.length,
    optimization: opt,
    max_mission_time_min: Math.max(...missions.map(m => m.stats.time_s / 60)),
    total_distance_km: missions.reduce((s, m) => s + m.stats.distance_m, 0) / 1000,
    total_area_km2: missions.reduce((s, m) => s + (m.metrics?.area_km2 || 0), 0),
    total_photos: missions.reduce((s, m) => s + (m.metrics?.photo_count || 0), 0),
    missions: missions.map(m => ({
      uav: m.uav_name,
      uav_id: m.uav_id,
      uav_type: m.uav_type,
      takeoff_type: m.takeoff_type,
      landing_type: m.landing_type,
      distance_km: +(m.stats.distance_m / 1000).toFixed(2),
      time_min: +(m.stats.time_s / 60).toFixed(1),
      waypoint_count: m.waypoints.length,
      warning: m.stats.warning,
      area_km2: m.metrics?.area_km2 || 0,
      gsd_cm: m.metrics?.gsd_cm || 0,
      strip_count: m.metrics?.strip_count || 0,
      photo_count: m.metrics?.photo_count || 0,
      swath_m: m.metrics?.swath_m || 0,
      altitude_m: m.altitude_m || 0,
      cost_rub_est: Math.round(m.stats.time_s / 3600 * 15000),
      start_latlon: m.start_latlon,
      land_latlon: m.land_latlon,
      assigned_zones: m.assigned_zones,
      n_zones: m.n_zones || 1,
      cruise_count: m.waypoints.filter(w => w.action === 'cruise').length,
      survey_pct: m.stats?.survey_pct || 0,
      photo_interval_m: m.metrics?.photo_interval_m || 0,
    })),
  };
}

// ─── Render comparison block ──────────────────────────────────────────────────
function renderComparison(cmp) {
  const el = document.getElementById('results-comparison');
  const mw = cmp.min_wear || cmp.min_flight;
  const better_time = cmp.min_time.max_mission_time_min <= mw.max_mission_time_min;
  const better_hours = (mw.total_flight_hours ?? Infinity) <= (cmp.min_time.total_flight_hours ?? Infinity);
  const better_dist_mt = cmp.min_time.total_distance_km <= mw.total_distance_km;

  const better_eff = (cmp.min_time.effective_cost_min ?? Infinity) <= (mw.effective_cost_min ?? Infinity);

  // Bar chart SVG
  const metrics = [
    { label: 'Время\n(мин)', mt: cmp.min_time.max_mission_time_min, mw: mw.max_mission_time_min },
    { label: 'Налёт\n(л/ч)', mt: (cmp.min_time.total_flight_hours||0)*60, mw: (mw.total_flight_hours||0)*60 },
    { label: 'Eff.\n(мин)', mt: cmp.min_time.effective_cost_min || cmp.min_time.total_distance_km, mw: mw.effective_cost_min || mw.total_distance_km },
  ];
  const bH = 72, bW = 18, gap = 5, groupW = bW*2+gap+22, svgW = groupW*metrics.length+30, svgH = bH + 46;
  let bars = '';
  metrics.forEach((m, i) => {
    const maxV = Math.max(m.mt, m.mw, 0.01);
    const hmt = Math.max((m.mt/maxV)*(bH-18), 2);
    const hmw = Math.max((m.mw/maxV)*(bH-18), 2);
    const x0 = 15 + i*groupW;
    bars += `
      <rect x="${x0}" y="${bH-hmt}" width="${bW}" height="${hmt}" fill="#3b82f6" opacity="0.8" rx="2"/>
      <rect x="${x0+bW+gap}" y="${bH-hmw}" width="${bW}" height="${hmw}" fill="#10b981" opacity="0.8" rx="2"/>
      <text x="${x0+bW/2}" y="${bH-hmt-2}" text-anchor="middle" fill="#3b82f6" font-size="7">${m.mt.toFixed(1)}</text>
      <text x="${x0+bW+gap+bW/2}" y="${bH-hmw-2}" text-anchor="middle" fill="#10b981" font-size="7">${m.mw.toFixed(1)}</text>
      <text x="${x0+bW+gap/2}" y="${bH+10}" text-anchor="middle" fill="#64748b" font-size="7">${m.label.split('\n')[0]}</text>
      <text x="${x0+bW+gap/2}" y="${bH+18}" text-anchor="middle" fill="#64748b" font-size="7">${m.label.split('\n')[1]||''}</text>
    `;
  });
  const chart = `<svg width="${svgW}" height="${svgH}" style="display:block;margin:6px auto 0">
    <line x1="10" y1="0" x2="10" y2="${bH}" stroke="#2e3352" stroke-width="1"/>
    <line x1="10" y1="${bH}" x2="${svgW-5}" y2="${bH}" stroke="#2e3352" stroke-width="1"/>
    ${bars}
    <rect x="15" y="${bH+18}" width="8" height="6" fill="#3b82f6" opacity="0.8" rx="1"/>
    <text x="26" y="${bH+24}" fill="#94a3b8" font-size="8">Мин. время</text>
    <rect x="90" y="${bH+18}" width="8" height="6" fill="#10b981" opacity="0.8" rx="1"/>
    <text x="101" y="${bH+24}" fill="#94a3b8" font-size="8">Мин. износ</text>
  </svg>`;

  // Smart recommendation
  const timeDiff = Math.abs(mw.max_mission_time_min - cmp.min_time.max_mission_time_min);
  const wearDiff = Math.abs((cmp.min_time.total_flight_hours - mw.total_flight_hours) * 60);
  const recText = timeDiff < 0.5 && wearDiff < 0.5
    ? '💡 Обе стратегии дают одинаковый результат для данной конфигурации'
    : better_eff
      ? `💡 Стратегия <b>Мин. время</b> быстрее на ${timeDiff.toFixed(1)} мин при разнице налёта ${wearDiff.toFixed(1)} мин`
      : `💡 Стратегия <b>Мин. износ</b> экономит ${wearDiff.toFixed(1)} мин ресурса БВС (дополнительные ${timeDiff.toFixed(1)} мин в пути)`;
  el.innerHTML = `
    <div style="font-size:10px;padding:5px 8px;background:rgba(59,130,246,0.06);border-radius:6px;border-left:3px solid var(--accent);margin-bottom:6px">${recText}</div>
    <div class="comparison-table">
      <div class="cmp-header">Показатель</div>
      <div class="cmp-header" style="color:#3b82f6">⏱ Мин. время</div>
      <div class="cmp-header" style="color:#10b981">🔧 Мин. износ</div>

      <div class="cmp-label">Время выполнения</div>
      <div class="cmp-val ${better_time ? 'cmp-best' : ''}">${cmp.min_time.max_mission_time_min.toFixed(1)} мин</div>
      <div class="cmp-val ${!better_time ? 'cmp-best' : ''}">${mw.max_mission_time_min.toFixed(1)} мин</div>

      <div class="cmp-label">Сумма л/ч</div>
      <div class="cmp-val ${!better_hours ? 'cmp-best' : ''}">${(cmp.min_time.total_flight_hours ?? '—')}</div>
      <div class="cmp-val ${better_hours ? 'cmp-best' : ''}">${(mw.total_flight_hours ?? '—')}</div>

      <div class="cmp-label">Общий налёт</div>
      <div class="cmp-val ${better_dist_mt ? 'cmp-best' : ''}">${cmp.min_time.total_distance_km.toFixed(2)} км</div>
      <div class="cmp-val ${!better_dist_mt ? 'cmp-best' : ''}">${mw.total_distance_km.toFixed(2)} км</div>

      ${cmp.min_time.effective_cost_min != null ? `
      <div class="cmp-label" title="Суммарный налёт + штраф за запуск × число БПЛА">Эфф. стоимость</div>
      <div class="cmp-val ${better_eff ? 'cmp-best' : ''}">${cmp.min_time.effective_cost_min.toFixed(1)} мин</div>
      <div class="cmp-val ${!better_eff ? 'cmp-best' : ''}">${mw.effective_cost_min.toFixed(1)} мин</div>
      ` : ''}
    </div>
    ${cmp.startup_cost_min != null ? `<div style="font-size:10px;color:var(--text2);margin:4px 0">Штраф за запуск: ${cmp.startup_cost_min} мин/БПЛА</div>` : ''}
    ${chart}
  `;
}

// ─── Render missions on map ───────────────────────────────────────────────────
function renderMissions(missions, geojson, summary) {
  state.currentMissions = missions;
  state.routeLayers.forEach(l => map.removeLayer(l));
  state.routeLayers = [];
  (state.rangeRings || []).forEach(l => map.removeLayer(l));
  state.rangeRings = [];
  if (state.photoGroup) { map.removeLayer(state.photoGroup); state.photoGroup = null; }
  // Draw range rings from each UAV start position
  missions.forEach((m, i) => {
    const spec = state.uavTypes.find(t => t.id === m.uav_id || t.id === m.uav_name);
    const rangeKm = spec?.max_range_km || (spec ? spec.cruise_speed_ms * spec.max_flight_time_min * 60 / 1000 / 2 : 0);
    const startLL = summary.missions?.[i]?.start_latlon;
    if (!startLL || !rangeKm) return;
    const color = ROUTE_COLORS[i % ROUTE_COLORS.length];
    const ring = L.circle([startLL[0], startLL[1]], {
      radius: rangeKm * 1000,
      color, weight: 1, opacity: 0.4, fillColor: color, fillOpacity: 0.03, dashArray: '6 4',
    });
    ring.bindTooltip(`${m.uav_name || m.uav_id}: макс. дальность ${rangeKm} км`, { sticky: true });
    ring.addTo(map);
    state.rangeRings.push(ring);
  });

  // Main route layer (exclude photo_line — rendered separately)
  const routeGroup = L.geoJSON(geojson, {
    filter: f => f.properties?.feature_type !== 'photo_line',
    style: feature => {
      const idx = feature.properties?.color_index ?? 0;
      const type = feature.properties?.feature_type;
      if (type === 'detour_segment') {
        return { color: '#f97316', weight: 3, dashArray: '10,5', opacity: 1 };
      }
      return {
        color: ROUTE_COLORS[idx % ROUTE_COLORS.length],
        weight: type === 'route' ? 2 : 1,
        opacity: type === 'route' ? 0.9 : 0.3,
        fillOpacity: 0.04,
        dashArray: type === 'sub_polygon' ? '4,4' : null,
      };
    },
    pointToLayer: (feature, latlng) => {
      const action = feature.properties?.action;
      const idx = feature.properties?.color_index ?? 0;
      const color = ROUTE_COLORS[idx % ROUTE_COLORS.length];
      if (action === 'cruise') {
        return L.circleMarker(latlng, {
          radius: 6, color: '#f97316', weight: 2, fillColor: '#f97316', fillOpacity: 0.85,
        }).bindPopup(`<b>${feature.properties.uav_id}</b><br/>Обход БЗ`);
      }
      const r = action === 'takeoff' ? 8 : action === 'rtl' ? 6 : 5;
      return L.circleMarker(latlng, {
        radius: r, color: '#fff', weight: 2, fillColor: color, fillOpacity: 1,
      }).bindPopup(`<b>${feature.properties.uav_id}</b><br/>${action}<br/>Фаза: ${feature.properties.phase ?? ''}`);
    },
    onEachFeature: (feature, layer) => {
      if (feature.properties?.feature_type === 'route') {
        layer.bindTooltip(
          `${feature.properties.uav_name}<br/>` +
          `${(feature.properties.distance_m / 1000).toFixed(1)} км | ` +
          `${(feature.properties.time_s / 60).toFixed(1)} мин`,
          { sticky: true }
        );
      }
    },
  }).addTo(map);
  state.routeLayers.push(routeGroup);

  // Photo coverage points layer (separate, toggleable)
  const photoFeatures = {
    type: 'FeatureCollection',
    features: (geojson.features || []).filter(f => f.properties?.feature_type === 'photo_line'),
  };
  if (photoFeatures.features.length > 0) {
    state.photoGroup = L.geoJSON(photoFeatures, {
      pointToLayer: (f, latlng) => {
        const color = ROUTE_COLORS[(f.properties?.color_index ?? 0) % ROUTE_COLORS.length];
        return L.circleMarker(latlng, {
          radius: 2, color, weight: 0, fillColor: color, fillOpacity: 0.55,
        });
      },
    });
    const showPhotos = document.getElementById('chk-photos')?.checked !== false;
    if (showPhotos) state.photoGroup.addTo(map);
    state.routeLayers.push(state.photoGroup);
  }

  try { map.fitBounds(routeGroup.getBounds().pad(0.1)); } catch {}
  renderSwathFootprints(missions);
  renderSummary(summary);
  checkTerrainClearance(summary);
}

// ─── Terrain clearance check (Open-Meteo elevation) ──────────────────────────
async function checkTerrainClearance(summary) {
  const missionAlt = parseFloat(document.getElementById('altitude')?.value || '150');
  const zones = state.areaPolygons.length ? state.areaPolygons : null;
  if (!zones) return;
  const pts = zones.flatMap(l => l.getLatLngs()[0] || []);
  if (!pts.length) return;
  const lats = pts.map(p => p.lat), lons = pts.map(p => p.lng);
  const minLat = Math.min(...lats), maxLat = Math.max(...lats);
  const minLon = Math.min(...lons), maxLon = Math.max(...lons);
  const midLat = (minLat + maxLat) / 2, midLon = (minLon + maxLon) / 2;

  // Terrain sample points: 4 corners + center
  const terrainLats = [minLat, maxLat, minLat, maxLat, midLat];
  const terrainLons = [minLon, minLon, maxLon, maxLon, midLon];

  // VPP points — query their AMSL elevation so we can compute true AGL clearance
  const startPts = (summary?.missions || [])
    .map(m => m.start_latlon)
    .filter(ll => ll && ll.length === 2);

  const allLats = [...terrainLats, ...startPts.map(ll => ll[0])];
  const allLons = [...terrainLons, ...startPts.map(ll => ll[1])];

  try {
    const res = await fetch(
      `https://api.open-meteo.com/v1/elevation?latitude=${allLats.map(v => v.toFixed(5)).join(',')}&longitude=${allLons.map(v => v.toFixed(5)).join(',')}`,
      { signal: AbortSignal.timeout(5000) },
    );
    if (!res.ok) return;
    const data = await res.json();
    const all = (data.elevation || []).filter(e => e != null);
    if (!all.length) return;

    const terrainElevs = all.slice(0, terrainLats.length);
    const vppElevs = all.slice(terrainLats.length);

    const maxElev = Math.max(...terrainElevs);
    const minElev = Math.min(...terrainElevs);
    const relief = maxElev - minElev;

    // True AGL clearance: drone flies missionAlt above its launch point (AMSL)
    // Use average VPP elevation if available, else min terrain (conservative estimate)
    const vppElev = vppElevs.length
      ? vppElevs.reduce((s, v) => s + v, 0) / vppElevs.length
      : minElev;
    const droneAMSL = vppElev + missionAlt;
    const clearance = droneAMSL - maxElev;

    state._terrainData = { maxElev, minElev, relief, clearance, vppElev };

    if (clearance < 30) {
      setStatus(`⛰ ВНИМАНИЕ: клиренс ${Math.round(clearance)} м над рельефом — увеличьте высоту!`, 'error');
    } else if (clearance < 80) {
      setStatus(`⛰ Клиренс ${Math.round(clearance)} м над рельефом (ВПП ${Math.round(vppElev)} м, рельеф до ${Math.round(maxElev)} м)`, 'ok');
    } else {
      setStatus(`⛰ Рельеф: ${Math.round(minElev)}–${Math.round(maxElev)} м, клиренс ${Math.round(clearance)} м ✅`, 'ok');
    }

    const kpiRow = document.querySelector('.summary-kpis');
    if (kpiRow) {
      let kpi = document.getElementById('kpi-terrain');
      if (!kpi) { kpi = document.createElement('div'); kpi.id = 'kpi-terrain'; kpi.className = 'kpi'; kpiRow.appendChild(kpi); }
      const clrColor = clearance < 30 ? '#ef4444' : clearance < 80 ? '#f59e0b' : '#10b981';
      kpi.title = `Клиренс над рельефом = высота AGL + AMSL ВПП − макс. рельеф. ВПП: ${Math.round(vppElev)} м, рельеф: ${Math.round(minElev)}–${Math.round(maxElev)} м, перепад: ${Math.round(relief)} м.`;
      kpi.innerHTML = `<span class="kpi-val" style="color:${clrColor}">${Math.round(clearance)}</span><span class="kpi-lbl">м клиренс</span>`;
    }
    // If clearance < 80m, show fix suggestion below the KPI row
    if (clearance < 80) {
      const safeAlt = Math.ceil((maxElev - vppElev + 80) / 10) * 10;
      let fixDiv = document.getElementById('terrain-fix-suggestion');
      if (!fixDiv) {
        fixDiv = document.createElement('div');
        fixDiv.id = 'terrain-fix-suggestion';
        fixDiv.style.cssText = 'margin:4px 0;padding:5px 8px;background:#ef444422;border-radius:6px;font-size:10px;color:var(--text)';
        kpiRow?.parentNode?.insertBefore(fixDiv, kpiRow.nextSibling);
      }
      const btnId = `btn-apply-safe-alt-${Date.now()}`;
      fixDiv.innerHTML = `⛰ Рельеф ${Math.round(maxElev)} м (ВПП ${Math.round(vppElev)} м) — клиренс ${Math.round(clearance)} м. Рекомендуемая высота: <b>${safeAlt} м AGL</b> <button id="${btnId}" style="margin-left:6px;padding:2px 8px;background:var(--accent);color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:10px">Применить</button>`;
      document.getElementById(btnId)?.addEventListener('click', () => {
        const altInput = document.getElementById('altitude');
        if (altInput) { altInput.value = safeAlt; altInput.dispatchEvent(new Event('input')); }
        fixDiv.remove();
        setStatus(`✅ Высота обновлена до ${safeAlt} м для безопасного клиренса над рельефом`, 'ok');
      });
    } else {
      document.getElementById('terrain-fix-suggestion')?.remove();
    }
  } catch {
    // API недоступна — тихая ошибка
  }
}

// ─── Swath footprint visualization ───────────────────────────────────────────
function renderSwathFootprints(missions) {
  (state.footprintLayers || []).forEach(l => map.removeLayer(l));
  state.footprintLayers = [];
  if (!document.getElementById('chk-footprints')?.checked) return;
  missions.forEach((m, mi) => {
    const swath = m.metrics?.swath_m;
    if (!swath) return;
    const color = ROUTE_COLORS[mi % ROUTE_COLORS.length];
    const startWps = (m.waypoints || []).filter(w => w.action === 'survey_start');
    const endWps = (m.waypoints || []).filter(w => w.action === 'survey_end');
    for (let i = 0; i < Math.min(startWps.length, endWps.length); i++) {
      const a = startWps[i], b = endWps[i];
      const midlat = (a.lat + b.lat) / 2 * Math.PI / 180;
      const dlat_m = (b.lat - a.lat) * 111320;
      const dlon_m = (b.lon - a.lon) * 111320 * Math.cos(midlat);
      const len = Math.sqrt(dlat_m * dlat_m + dlon_m * dlon_m) || 1;
      const pn = -dlon_m / len, pe = dlat_m / len;
      const hw = swath / 2;
      const pLat = pn * hw / 111320;
      const pLon = pe * hw / (111320 * Math.cos(midlat));
      const corners = [
        [a.lat + pLat, a.lon + pLon],
        [b.lat + pLat, b.lon + pLon],
        [b.lat - pLat, b.lon - pLon],
        [a.lat - pLat, a.lon - pLon],
      ];
      const poly = L.polygon(corners, { color, fillColor: color, fillOpacity: 0.18, weight: 0.8, opacity: 0.4 });
      state.footprintLayers.push(poly);
      poly.addTo(map);
    }
  });
}

function renderSummary(summary) {
  const panel = document.getElementById('results-panel');
  const container = document.getElementById('results-summary');
  panel.style.display = '';

  const optLabel = summary.optimization === 'min_time' ? 'Мин. время' : 'Мин. налёт';
  const _totalCost = (summary.missions || []).reduce((s, m) => s + (m.cost_rub_est || 0), 0);
  const _maxMissionTime = Math.max(...(summary.missions || []).map(m => m.time_min || 0), 1);
  const _ganttW = 188;
  const _ganttH = (summary.missions || []).length * 20 + 8;
  const _ganttSvg = (summary.missions || []).length > 1 ? `
    <svg width="${_ganttW + 80}" height="${_ganttH}" viewBox="0 0 ${_ganttW + 80} ${_ganttH}" style="display:block;width:100%;margin:6px 0 2px" title="Временная диаграмма миссий">
      <rect x="0" y="0" width="${_ganttW}" height="${_ganttH}" rx="2" fill="var(--surface2)"/>
      ${(summary.missions || []).map((m, i) => {
        const bw = Math.max(4, Math.round(m.time_min / _maxMissionTime * _ganttW));
        const y = 4 + i * 20;
        const col = ROUTE_COLORS[i % ROUTE_COLORS.length];
        return `<rect x="0" y="${y}" width="${bw}" height="12" rx="2" fill="${col}" opacity="0.85"/>
          <text x="${bw + 4}" y="${y + 9}" font-size="9" fill="var(--text2)" font-family="sans-serif">${m.time_min} мин</text>`;
      }).join('')}
    </svg>` : '';
  container.innerHTML = `
    <div class="summary-total">
      <div class="summary-kpis">
        <div class="kpi"><span class="kpi-val">${summary.total_uavs}</span><span class="kpi-lbl">БВС</span></div>
        <div class="kpi"><span class="kpi-val">${summary.max_mission_time_min.toFixed(0)}</span><span class="kpi-lbl">мин макс</span></div>
        <div class="kpi"><span class="kpi-val">${summary.total_distance_km.toFixed(1)}</span><span class="kpi-lbl">км налёт</span></div>
        <div class="kpi"><span class="kpi-val">${(summary.total_area_km2 || 0).toFixed(2)}</span><span class="kpi-lbl">км² покр.</span></div>
        ${_totalCost > 0 ? `<div class="kpi"><span class="kpi-val">${Math.round(_totalCost/1000)}</span><span class="kpi-lbl">тыс. ₽</span></div>` : ''}
        ${_totalCost > 0 && summary.total_area_km2 > 0 ? `<div class="kpi"><span class="kpi-val">${Math.round(_totalCost/summary.total_area_km2/1000)}</span><span class="kpi-lbl">тыс./км²</span></div>` : ''}
        ${summary.total_photos > 0 ? `<div class="kpi"><span class="kpi-val">${summary.total_photos > 999 ? (summary.total_photos/1000).toFixed(1)+'k' : summary.total_photos}</span><span class="kpi-lbl">снимков</span></div>` : ''}
        ${summary.total_photos > 0 ? `<div class="kpi"><span class="kpi-val">${(summary.total_photos * 15 / 1024).toFixed(1)}</span><span class="kpi-lbl">ГБ данных</span></div>` : ''}
        ${summary.total_photos > 0 ? `<div class="kpi" title="Ориентировочное время обработки в Agisoft Metashape (4-ядерный ПК)"><span class="kpi-val">${Math.ceil(summary.total_photos / 500)}</span><span class="kpi-lbl">ч обработки</span></div>` : ''}
      </div>
      ${_ganttSvg}
      ${(() => {
        const missions = summary.missions || [];
        if (!missions.length) return '';
        const avgSurvey = missions.reduce((s, m) => s + (m.survey_pct || 0), 0) / missions.length;
        const transit = 100 - avgSurvey;
        // Donut SVG: R=28, stroke-width=12
        const R = 28, C = 2 * Math.PI * R;
        const surveyArc = C * avgSurvey / 100;
        return `<div style="display:flex;align-items:center;gap:8px;margin-top:4px">
          <svg width="68" height="68" viewBox="0 0 68 68" style="flex-shrink:0">
            <circle cx="34" cy="34" r="${R}" fill="none" stroke="var(--surface2)" stroke-width="12"/>
            <circle cx="34" cy="34" r="${R}" fill="none" stroke="#3b82f6" stroke-width="12"
              stroke-dasharray="${surveyArc.toFixed(1)} ${C.toFixed(1)}" stroke-dashoffset="${(C/4).toFixed(1)}" transform="rotate(-90 34 34)"/>
            <text x="34" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="var(--text)">${Math.round(avgSurvey)}%</text>
          </svg>
          <div style="font-size:9px;color:var(--text2)">
            <div><span style="color:#3b82f6;font-weight:700">■</span> Съёмка ${Math.round(avgSurvey)}%</div>
            <div><span style="color:var(--text2)">■</span> Транзит ${Math.round(transit)}%</div>
            <div style="margin-top:3px;color:var(--text2)">КПД маршрута</div>
          </div>
        </div>`;
      })()}
    </div>
    ${summary.missions.map((m, i) => {
      const uavSpec = state.uavTypes.find(t => t.id === m.uav_id);
      const maxTime = uavSpec?.max_flight_time_min || null;
      const windFactor = m.wind_power_factor || 1.0;
      const battPct = maxTime ? Math.round(m.time_min / maxTime * 100 * windFactor) : null;
      const battColor = !battPct ? '#10b981' : battPct > 85 ? '#ef4444' : battPct > 70 ? '#f59e0b' : '#10b981';
      // Altitude profile SVG
      const _wps = (state.currentMissions || [])[i]?.waypoints || [];
      const _nav = _wps.filter(w => ['takeoff','climb','cruise','survey_start','survey_end','rtl','land'].includes(w.action));
      let _altPts = [], _dist = 0;
      const _ER = 6371000;
      for (let _j = 0; _j < _nav.length; _j++) {
        if (_j > 0) {
          const _a = _nav[_j-1], _b = _nav[_j];
          const _dlat = (_b.lat - _a.lat) * Math.PI / 180;
          const _dlon = (_b.lon - _a.lon) * Math.PI / 180;
          const _mlat = (_a.lat + _b.lat) / 2 * Math.PI / 180;
          _dist += Math.sqrt((_dlat * _ER) ** 2 + (_dlon * _ER * Math.cos(_mlat)) ** 2);
        }
        _altPts.push({ d: _dist, alt: _nav[_j].alt_m || 0 });
      }
      let _altSvg = '';
      if (_altPts.length > 1) {
        const _W = 196, _H = 36;
        const _maxD = _altPts[_altPts.length - 1].d || 1;
        // Include terrain in max scale if available
        const _terrainAMSL = state._terrainData?.maxElev;
        const _vppElev = state._terrainData?.vppElev || 0;
        const _maxFlightAlt = Math.max(..._altPts.map(p => p.alt));
        const _maxA = _maxFlightAlt * 1.15 || 200;
        const _tx = d => (_d => Math.round(_d / _maxD * _W))(d);
        const _ty = a => Math.round(_H - (a / _maxA) * _H);
        const _pts = _altPts.map(p => `${_tx(p.d)},${_ty(p.alt)}`).join(' ');
        const _fill = _altPts.map((p, k) => k === 0 ? `M${_tx(p.d)},${_ty(p.alt)}` : `L${_tx(p.d)},${_ty(p.alt)}`).join(' ') + ` L${_W},${_H} L0,${_H} Z`;
        // Terrain line: terrain AGL = maxTerrainAMSL - vppElev
        const _terrainAGL = _terrainAMSL != null ? Math.max(0, _terrainAMSL - _vppElev) : null;
        const _terrainY = _terrainAGL != null && _terrainAGL < _maxA ? _ty(_terrainAGL) : null;
        const _terrainSvg = _terrainY != null ? `
          <rect x="0" y="${_terrainY}" width="${_W}" height="${_H - _terrainY}" fill="#92400e" opacity="0.15"/>
          <line x1="0" y1="${_terrainY}" x2="${_W}" y2="${_terrainY}" stroke="#92400e" stroke-width="1" stroke-dasharray="3,2" opacity="0.7"/>
          <text x="${_W - 2}" y="${_terrainY - 2}" text-anchor="end" font-size="6" fill="#92400e" opacity="0.8">рельеф ${Math.round(_terrainAGL)}м</text>` : '';
        _altSvg = `<svg width="${_W}" height="${_H}" viewBox="0 0 ${_W} ${_H}" style="display:block;width:100%;margin:5px 0 2px;border-radius:3px;background:var(--surface2);opacity:0.9" title="Профиль высоты маршрута${_terrainAGL != null ? ` | Рельеф: ${Math.round(_terrainAGL)} м AGL` : ''}">
          <defs><linearGradient id="ag${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3b82f6" stop-opacity="0.5"/><stop offset="100%" stop-color="#3b82f6" stop-opacity="0.05"/></linearGradient></defs>
          ${_terrainSvg}
          <path d="${_fill}" fill="url(#ag${i})"/>
          <polyline points="${_pts}" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linejoin="round"/>
        </svg>`;
      }
      const _batt = battPct != null ? Math.max(0, Math.min(100, 120 - battPct)) : 70;
      const _surv = m.survey_pct || 70;
      const _nfz = m.cruise_count > 0 ? 70 : 100;
      const _gsd = m.gsd_cm ? (m.gsd_cm <= 2 ? 100 : m.gsd_cm <= 5 ? 85 : m.gsd_cm <= 10 ? 65 : 40) : 75;
      const feasScore = Math.round(_batt * 0.4 + _surv * 0.3 + _nfz * 0.15 + _gsd * 0.15);
      const feasColor = feasScore >= 80 ? '#10b981' : feasScore >= 60 ? '#f59e0b' : '#ef4444';
      const feasLabel = feasScore >= 80 ? 'Отлично' : feasScore >= 60 ? 'Пригоден' : 'Риск';
      return `
      <div class="mission-card ${m.warning ? 'warn' : ''}">
        <div class="mc-header">
          <span class="mc-dot" style="background:${ROUTE_COLORS[i % ROUTE_COLORS.length]}"></span>
          <strong>${m.uav}</strong>
          ${m.warning ? `<span class="warn-badge">⚠ Батарея</span>` : ''}
          ${m.cruise_count > 0 ? `<span class="nfz-bypass-badge">⚡ Обход БЗ (${m.cruise_count} тч.)</span>` : ''}
          <span style="font-size:10px;font-weight:700;color:${feasColor};background:${feasColor}22;padding:2px 7px;border-radius:10px;white-space:nowrap">${feasScore} ${feasLabel}</span>
          <button class="btn-anim" data-anim="${i}" title="Анимировать маршрут" style="background:none;border:none;cursor:pointer;font-size:13px;color:var(--accent);padding:0 4px;line-height:1">▶</button>
        </div>
        <div class="mc-grid">
          <div class="mc-item"><span class="mc-val">${m.distance_km}</span><span class="mc-lbl">км</span></div>
          <div class="mc-item"><span class="mc-val">${m.time_min >= 60 ? `${Math.floor(m.time_min/60)}ч${Math.round(m.time_min%60)}м` : m.time_min}</span><span class="mc-lbl">${m.time_min >= 60 ? 'налёт' : 'мин'}</span></div>
          <div class="mc-item"><span class="mc-val">${m.area_km2 || '—'}</span><span class="mc-lbl">км²</span></div>
          <div class="mc-item"><span class="mc-val">${m.gsd_cm || '—'}</span><span class="mc-lbl">см/пкс</span></div>
          <div class="mc-item"><span class="mc-val">${m.strip_count || 0}</span><span class="mc-lbl">маршрутов</span></div>
          <div class="mc-item"><span class="mc-val">${m.photo_count || 0}</span><span class="mc-lbl">снимков</span></div>
          ${m.photo_interval_m ? `<div class="mc-item"><span class="mc-val">${m.photo_interval_m}</span><span class="mc-lbl">м/снимок</span></div>` : ''}
        </div>
        ${_altSvg}
        ${(() => {
          const gsd = m.gsd_cm;
          if (!gsd) return '';
          const cls = gsd <= 2 ? '🏆 Кадастр / инженерные изыскания' : gsd <= 5 ? '✅ ГИС / ортофото' : gsd <= 10 ? '📊 Мониторинг' : '🔍 Обзорная съёмка';
          const clr = gsd <= 2 ? '#10b981' : gsd <= 5 ? '#3b82f6' : gsd <= 10 ? '#f59e0b' : '#94a3b8';
          return `<div style="font-size:10px;padding:3px 10px;color:${clr};font-weight:600">${cls} (GSD ${gsd} см)</div>`;
        })()}
        <div class="mc-footer">
          Взлёт: ${_takeoffLabel(m.takeoff_type)} &nbsp;|&nbsp; Посадка: ${_landLabel(m.landing_type)}
          ${m.altitude_m ? `&nbsp;|&nbsp; H: ${m.altitude_m} м` : ''}
          ${(m.n_zones || 1) > 1 ? `<br/>Зоны: ${m.n_zones} (${(m.assigned_zones||[]).map(z=>z+1).join(', ')})` : ''}
          ${battPct != null ? `
          <div class="battery-row">
            <span class="battery-lbl">🔋 ${battPct}%</span>
            <div class="battery-bar-outer"><div class="battery-bar-inner" style="width:${Math.min(100,battPct)}%;background:${battColor}"></div></div>
          </div>
          ${battPct > 100 ? (() => {
            const legs = Math.ceil(battPct / 100);
            const legMin = Math.round(m.time_min / legs);
            const rechargeMin = 60;
            const totalElapsed = m.time_min + (legs - 1) * rechargeMin;
            const legSteps = Array.from({length: legs}, (_, k) => {
              const start = k * (legMin + rechargeMin);
              const end = start + legMin;
              return `Вылет ${k+1}: ${start}–${end} мин`;
            }).join(' → ');
            return `<div style="font-size:10px;color:#ef4444;font-weight:600;padding:3px 0">⚠ Нужно ${legs} вылета (${battPct}% ресурса)</div>
            <div style="font-size:9px;color:var(--text2);padding:2px 0;line-height:1.5">${legSteps}<br/>+ ${legs-1} дозарядки по ~${rechargeMin} мин = ~${Math.round(totalElapsed/60*10)/10} ч всего</div>`;
          })() : ''}` : ''}
          ${m.survey_pct > 0 ? `<br/>КПД маршрута: <b>${m.survey_pct}%</b> съёмка / ${100 - m.survey_pct}% транзит${m.survey_pct < 65 ? ' <span style="color:#f59e0b">⚠ рассмотрите ВПП ближе к зоне</span>' : ''}` : ''}
          ${m.cost_rub_est ? `<br/>Оценка ресурса: ~${(m.cost_rub_est/1000).toFixed(1)} тыс. руб.` : ''}
          ${(() => {
            const dv = document.getElementById('departure-time')?.value || '09:00';
            const [dh, dm] = dv.split(':').map(Number);
            const base = dh * 60 + dm;
            const land = base + Math.round(m.time_min);
            const lh = Math.floor(land / 60) % 24, lm = land % 60;
            const sunEl = (() => {
              if (!m.start_latlon) return null;
              const lat = m.start_latlon[0] * Math.PI / 180;
              const now2 = new Date();
              const doy = Math.floor((now2 - new Date(now2.getFullYear(), 0, 0)) / 86400000);
              const decl = 23.45 * Math.sin((360 / 365 * (doy - 81)) * Math.PI / 180) * Math.PI / 180;
              const ha = (dh + dm / 60 - 12) * 15 * Math.PI / 180;
              return Math.asin(Math.sin(lat) * Math.sin(decl) + Math.cos(lat) * Math.cos(decl) * Math.cos(ha)) * 180 / Math.PI;
            })();
            const sunWarn = sunEl !== null && sunEl < 20 ? `<span style="color:#f59e0b"> ⚠ Солнце ${sunEl.toFixed(0)}° — плохое освещение</span>` :
              sunEl !== null && sunEl > 60 ? `<span style="color:#f59e0b"> ⚠ Солнце ${sunEl.toFixed(0)}° — жёсткие тени</span>` : '';
            return `<div style="font-size:10px;margin-top:2px">🕐 Вылет ${dv} → Посадка ${String(lh).padStart(2,'0')}:${String(lm).padStart(2,'0')}${sunWarn}</div>`;
          })()}
          ${m.start_latlon ? `<br/>Старт: ${m.start_latlon[0].toFixed(5)}, ${m.start_latlon[1].toFixed(5)}` : ''}
          ${m.strip_angle_deg != null ? `<br/>Угол съёмки: <b>${Math.round(m.strip_angle_deg)}°</b> <span style="color:var(--text2);font-size:9px">(оптим. по форме зоны и ветру)</span>` : ''}
          ${(() => {
            if (!state.reserveMarkers.length || !m.land_latlon) return '';
            const [lLat, lLon] = m.land_latlon;
            let minDist = Infinity;
            state.reserveMarkers.forEach(rm => {
              const rLL = rm.getLatLng();
              const dlat = (rLL.lat - lLat) * 111320;
              const dlon = (rLL.lng - lLon) * 111320 * Math.cos(lLat * Math.PI / 180);
              minDist = Math.min(minDist, Math.sqrt(dlat*dlat + dlon*dlon));
            });
            return `<div style="font-size:10px;color:var(--text2);margin-top:2px">🛬 Резерв в ${(minDist/1000).toFixed(1)} км от точки посадки</div>`;
          })()}
        </div>
      </div>
    `;}).join('')}
  ${(() => {
    const recs = [];
    const missions = summary.missions || [];
    missions.forEach(m => {
      const spec = state.uavTypes.find(t => t.id === m.uav_id);
      const bPct = spec ? m.time_min / spec.max_flight_time_min * 100 * (m.wind_power_factor || 1) : 0;
      if (bPct > 85) recs.push(`🔋 ${m.uav}: расход заряда ${Math.round(bPct)}% — сократите зону или добавьте дозаправку`);
      if ((m.survey_pct || 0) < 55) recs.push(`📍 ${m.uav}: КПД съёмки ${m.survey_pct}% — перенесите ВПП ближе к зоне`);
    });
    if (summary.max_mission_time_min > 60) recs.push(`⏱ Время выполнения ${Math.round(summary.max_mission_time_min)} мин — рассмотрите добавление БВС для параллельной съёмки`);
    const avgGsd = missions.reduce((s,m) => s+(m.gsd_cm||0), 0) / (missions.length||1);
    if (avgGsd > 12) recs.push(`🔭 GSD ${avgGsd.toFixed(1)} см — снижение высоты на 20-30% улучшит детальность снимков`);
    const maxBattPct = Math.max(...missions.map(m => {
      const spec = state.uavTypes.find(t => t.id === m.uav_id);
      return spec ? m.time_min / spec.max_flight_time_min * 100 * (m.wind_power_factor || 1) : 0;
    }));
    if (maxBattPct > 100) {
      const curAlt = +document.getElementById('altitude').value || 150;
      const suggestAlt = Math.ceil(curAlt * maxBattPct / 85 / 10) * 10;
      const newGsd = (avgGsd * suggestAlt / curAlt).toFixed(1);
      recs.push(`🔭 Для покрытия за 1 вылет — увеличьте высоту до ${suggestAlt} м (GSD ≈ ${newGsd} см, расход ≈ 85%)`);
    }
    if (summary.total_area_km2 > 15 && summary.total_uavs === 1) {
      recs.push(`✈️ Площадь ${summary.total_area_km2.toFixed(1)} км² — добавьте 2-й БВС для параллельной съёмки и сокращения времени вдвое`);
    }
    const recsHtml = recs.length ? `<div style="margin-top:6px;padding:7px 10px;background:rgba(59,130,246,0.06);border-radius:6px;border-left:3px solid var(--accent)">
      <div style="font-size:10px;font-weight:700;color:var(--text2);margin-bottom:4px">💡 РЕКОМЕНДАЦИИ</div>
      ${recs.map(r => `<div style="font-size:10px;color:var(--text);margin-bottom:3px">${r}</div>`).join('')}
    </div>` : '';
    // What-if wind analysis
    const windSpeeds = [0, 5, 10, 15];
    const whatIfRows = missions.map(m => {
      const spec = state.uavTypes.find(t => t.id === m.uav_id);
      if (!spec) return '';
      const v = spec.cruise_speed_ms;
      const cells = windSpeeds.map(w => {
        let wpf = 1.0;
        if (w > 0 && v > 0) {
          const vh = v + w, vt = Math.max(v - w, 1);
          wpf = ((vh**2.5 + vt**2.5) / 2) / (v**2.5);
        }
        const bp = Math.round(m.time_min / spec.max_flight_time_min * 100 * wpf);
        const clr = bp > 100 ? '#ef4444' : bp > 85 ? '#f59e0b' : '#10b981';
        return `<td style="text-align:center;color:${clr};font-weight:${bp>85?'700':'400'}">${bp}%${w > spec.max_wind_ms ? '<br/><span style="font-size:8px;color:#ef4444">⛔</span>' : ''}</td>`;
      }).join('');
      return `<tr><td style="font-size:9px;color:var(--text2);padding-right:4px">${m.uav}</td>${cells}</tr>`;
    }).join('');
    const whatIfHtml = whatIfRows ? `<div style="margin-top:6px">
      <div style="font-size:10px;font-weight:700;color:var(--text2);margin-bottom:4px">🌬 АНАЛИЗ ВЕТРОВОЙ НАГРУЗКИ</div>
      <table style="width:100%;border-collapse:collapse;font-size:10px">
        <thead><tr style="color:var(--text2)"><th></th>${windSpeeds.map(w=>`<th style="text-align:center">${w} м/с</th>`).join('')}</tr></thead>
        <tbody>${whatIfRows}</tbody>
      </table>
      <div style="font-size:9px;color:var(--text2);margin-top:3px">% заряда аккумулятора при разных скоростях ветра. ⛔ = превышен лимит БВС.</div>
    </div>` : '';
    return recsHtml + whatIfHtml;
  })()}
  `;
  // Bind animation buttons after innerHTML is set
  container.querySelectorAll('[data-anim]').forEach(btn => {
    btn.addEventListener('click', () => animateMission(+btn.dataset.anim));
  });
}

// ─── Mission animation ────────────────────────────────────────────────────────
let _animHandle = null;
function animateMission(missionIdx) {
  const m = state.currentMissions?.[missionIdx];
  if (!m) return;
  const wps = (m.waypoints || []).filter(w => w.action !== 'photo');
  if (wps.length < 2) return;

  // Build path with cumulative distances
  const ER = 6371000;
  const path = [];
  let totalDist = 0;
  for (let i = 0; i < wps.length; i++) {
    if (i > 0) {
      const a = wps[i - 1], b = wps[i];
      const dlat = (b.lat - a.lat) * Math.PI / 180;
      const dlon = (b.lon - a.lon) * Math.PI / 180;
      const mlat = (a.lat + b.lat) / 2 * Math.PI / 180;
      totalDist += Math.sqrt((dlat * ER) ** 2 + (dlon * ER * Math.cos(mlat)) ** 2);
    }
    path.push({ lat: wps[i].lat, lon: wps[i].lon, d: totalDist });
  }

  const color = ROUTE_COLORS[missionIdx % ROUTE_COLORS.length];
  const icon = L.divIcon({
    html: `<div style="font-size:18px;filter:drop-shadow(0 0 4px ${color}) drop-shadow(0 0 8px white);transform:rotate(45deg)">✈</div>`,
    className: '', iconSize: [22, 22], iconAnchor: [11, 11],
  });
  const marker = L.marker([path[0].lat, path[0].lon], { icon, zIndexOffset: 1000 }).addTo(map);

  // Center map on start
  map.panTo([path[0].lat, path[0].lon], { animate: true, duration: 0.5 });

  if (_animHandle) cancelAnimationFrame(_animHandle);
  const DURATION_MS = Math.min(12000, Math.max(5000, m.stats?.time_s ? m.stats.time_s * 10 : 8000));
  const startTime = performance.now();

  function step(now) {
    const t = Math.min((now - startTime) / DURATION_MS, 1);
    const d = t * totalDist;
    let seg = 0;
    while (seg < path.length - 2 && path[seg + 1].d <= d) seg++;
    const a = path[seg], b = path[seg + 1];
    const segLen = b.d - a.d;
    const frac = segLen > 0 ? (d - a.d) / segLen : 0;
    marker.setLatLng([a.lat + (b.lat - a.lat) * frac, a.lon + (b.lon - a.lon) * frac]);
    if (t < 1) {
      _animHandle = requestAnimationFrame(step);
    } else {
      map.removeLayer(marker);
      setStatus('Анимация завершена', 'ok');
    }
  }
  _animHandle = requestAnimationFrame(step);
  setStatus('Анимация маршрута…', 'loading');
}

// ─── Pre-flight checklist ─────────────────────────────────────────────────────
function showPreflightChecklist() {
  const windOk = (() => {
    const ws = parseFloat(document.getElementById('wind-speed')?.value || '0');
    const uavMax = Math.min(...(state.uavRows || []).map(r => {
      const spec = state.uavTypes.find(t => t.id === r.typeId);
      return spec?.max_wind_ms || 12;
    }).filter(v => v > 0), 12);
    return ws <= uavMax * 0.8;
  })();
  const battOk = (() => {
    return (state.lastResult?.summary?.missions || []).every(m => {
      const spec = state.uavTypes.find(t => t.id === m.uav_id);
      if (!spec) return true;
      return m.time_min / spec.max_flight_time_min * 100 * (m.wind_power_factor || 1) < 85;
    });
  })();
  const mapCenter = map.getCenter();
  const notamUrl = `https://www.notam.ru/?lat=${mapCenter.lat.toFixed(4)}&lon=${mapCenter.lng.toFixed(4)}`;
  const items = [
    '✈️ БПЛА в сборе, механика и крепления проверены',
    '🔋 Аккумулятор заряжен не менее 90%',
    '🛰️ GPS-фикс получен (не менее 8 спутников)',
    '📷 Полезная нагрузка установлена и включена',
    `🌬️ Скорость ветра в допустимых пределах для БВС ${windOk ? '✅' : '⚠️ — проверьте!'}`,
    `⛔ Бесполётные зоны перепроверены по актуальным NOTAM — <a href="${notamUrl}" target="_blank" style="color:#3b82f6">Открыть NOTAM</a>`,
    '📡 Связь с наземной станцией управления установлена',
    '🗺️ Маршрут загружен и верифицирован в системе управления',
    '🏁 Площадка взлёта/посадки очищена и безопасна',
    '📋 Разрешение на использование воздушного пространства получено',
    `🔋 Расчётный расход заряда < 85%${battOk ? ' ✅' : ' ⚠️ — проверьте!'}`,
  ];
  const existing = document.getElementById('preflight-modal');
  if (existing) { existing.remove(); return; }
  const modal = document.createElement('div');
  modal.id = 'preflight-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;display:flex;align-items:center;justify-content:center';
  modal.innerHTML = `<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px;max-width:420px;width:92%;max-height:82vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.5)">
    <h3 style="margin:0 0 16px;font-size:15px;color:var(--text)">🔧 Pre-flight Checklist</h3>
    <div id="pf-items">${items.map((item, i) => `<label style="display:flex;align-items:flex-start;gap:10px;margin:10px 0;cursor:pointer;font-size:12px;color:var(--text);line-height:1.4"><input type="checkbox" data-pf="${i}" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"/>${item}</label>`).join('')}</div>
    <div id="pf-status" style="margin-top:12px;font-size:11px;color:var(--text2)">Отмечено: 0/${items.length}</div>
    <div style="display:flex;gap:8px;margin-top:16px">
      <button id="pf-confirm" class="btn btn-success" style="flex:1;opacity:0.4;cursor:not-allowed" disabled>✅ К полёту готов</button>
      <button id="pf-close" class="btn btn-ghost" style="flex:1">Закрыть</button>
    </div>
  </div>`;
  document.body.appendChild(modal);
  const cbs = modal.querySelectorAll('[data-pf]');
  const confirmBtn = modal.querySelector('#pf-confirm');
  const statusEl = modal.querySelector('#pf-status');
  function updateStatus() {
    const n = [...cbs].filter(c => c.checked).length;
    if (n === items.length) {
      statusEl.style.color = '#10b981'; statusEl.textContent = '✅ Все пункты выполнены — можно взлетать!';
      confirmBtn.disabled = false; confirmBtn.style.opacity = '1'; confirmBtn.style.cursor = '';
    } else {
      statusEl.style.color = 'var(--text2)'; statusEl.textContent = `Отмечено: ${n}/${items.length}`;
    }
  }
  cbs.forEach(cb => cb.addEventListener('change', updateStatus));
  modal.querySelector('#pf-close').addEventListener('click', () => modal.remove());
  confirmBtn.addEventListener('click', () => { modal.remove(); setStatus('✅ Pre-flight чеклист пройден — полёт разрешён!', 'ok'); });
  modal.addEventListener('click', e => { if (e.target === modal) modal.remove(); });
}

function _takeoffLabel(t) {
  return t === 'catapult' ? 'Катапульта' : t === 'vtol' ? 'ВТОЛ' : t || '—';
}
function _landLabel(t) {
  return t === 'parachute' ? 'Парашют' : t === 'vtol' ? 'ВТОЛ' : t || '—';
}

// ─── Export ──────────────────────────────────────────────────────────────────
async function exportPlan(format, opt) {
  if (!state.lastRequest) return;
  const req = { ...state.lastRequest, optimization: opt };
  const endpoint = format === 'kml' ? '/api/export/kml' : '/api/export/geojson';
  const ext = format === 'kml' ? 'kml' : 'geojson';
  const label = opt === 'min_time' ? 'time' : opt === 'min_wear' ? 'wear' : opt;
  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });
    if (!resp.ok) throw new Error(await resp.text());
    downloadBlob(await resp.blob(), `flight_plan_${label}.${ext}`);
  } catch (e) { setStatus(`Ошибка экспорта: ${e.message}`, 'error'); }
}

document.getElementById('btn-export-kml').addEventListener('click', () => {
  const opt = state.lastRequest?.optimization || 'min_time';
  exportPlan('kml', opt === 'both' ? 'min_time' : opt);
});
document.getElementById('btn-export-geojson').addEventListener('click', () => {
  const opt = state.lastRequest?.optimization || 'min_time';
  exportPlan('geojson', opt === 'both' ? 'min_time' : opt);
});
document.getElementById('btn-export-mavlink').addEventListener('click', () => {
  exportMAVLink(state.currentMissions);
});
document.getElementById('btn-export-report').addEventListener('click', () => {
  generateMissionReport(state.currentMissions, state.lastResult?.summary);
});
document.getElementById('btn-preflight').addEventListener('click', showPreflightChecklist);
document.getElementById('btn-gcp')?.addEventListener('click', placeGCPs);
document.getElementById('btn-weather')?.addEventListener('click', fetchWeather);
document.getElementById('btn-alt-calc')?.addEventListener('click', showAltCalc);

// ─── GCP Placement ────────────────────────────────────────────────────────────
function placeGCPs() {
  if (!state.areaPolygons.length) { setStatus('Сначала задайте зону съёмки', 'error'); return; }
  (state.gcpMarkers || []).forEach(m => map.removeLayer(m));
  state.gcpMarkers = [];
  const allPts = state.areaPolygons.flatMap(l => l.getLatLngs()[0] || []);
  if (!allPts.length) return;
  const lats = allPts.map(p => p.lat), lons = allPts.map(p => p.lng);
  const minLat = Math.min(...lats), maxLat = Math.max(...lats);
  const minLon = Math.min(...lons), maxLon = Math.max(...lons);
  const area_km2 = (maxLat - minLat) * 111.32 * (maxLon - minLon) * 111.32 * Math.cos((minLat + maxLat) / 2 * Math.PI / 180);
  const gridN = area_km2 > 10 ? 4 : 3;
  const pts = [];
  for (let gy = 0; gy <= gridN; gy++) {
    for (let gx = 0; gx <= gridN; gx++) {
      const lat = minLat + (maxLat - minLat) * gy / gridN;
      const lon = minLon + (maxLon - minLon) * gx / gridN;
      pts.push([lat, lon]);
    }
  }
  const perimeter = [[minLat, minLon], [minLat, maxLon], [maxLat, maxLon], [maxLat, minLon]];
  const allSelected = [...pts, ...perimeter];
  const deduped = allSelected.filter((p, i, arr) =>
    arr.findIndex(q => Math.abs(q[0]-p[0]) < 0.0001 && Math.abs(q[1]-p[1]) < 0.0001) === i
  );
  deduped.forEach((p, idx) => {
    const icon = L.divIcon({
      html: `<div style="background:#f59e0b;color:#000;font-size:9px;font-weight:700;border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.5)">G${idx+1}</div>`,
      className: '', iconSize: [18, 18], iconAnchor: [9, 9],
    });
    const m = L.marker(p, { icon }).addTo(map);
    m.bindTooltip(`ГКТ ${idx+1}: ${p[0].toFixed(5)}, ${p[1].toFixed(5)}`);
    state.gcpMarkers.push(m);
  });
  const csvRows = ['ID,Lat,Lon,Alt_m,Description'];
  deduped.forEach((p, i) => csvRows.push(`GCP${i+1},${p[0].toFixed(6)},${p[1].toFixed(6)},0,Наземная контрольная точка`));
  state._gcpCsv = csvRows.join('\n');
  setStatus(`📍 Расставлено ${deduped.length} ГКТ — <a href="#" id="_gcp_dl" style="color:var(--accent)">Скачать CSV</a>`, 'ok');
  setTimeout(() => {
    document.getElementById('_gcp_dl')?.addEventListener('click', e => {
      e.preventDefault();
      downloadBlob(new Blob([state._gcpCsv], { type: 'text/csv' }), 'gcp_points.csv');
    });
  }, 100);
}

// ─── Altitude / GSD calculator ───────────────────────────────────────────────
function showAltCalc() {
  document.getElementById('alt-calc-popup')?.remove();
  const uavSel = state.uavTypes[0];
  const payloadSel = state.payloadSpecs?.['rgb'];
  // Build UAV options
  const uavOpts = state.uavTypes.map(u =>
    `<option value="${u.id}" data-f="${u.focal_mm||35}" data-sw="${u.sensor_w_mm||35.9}">${u.name}</option>`
  ).join('');
  const popup = document.createElement('div');
  popup.id = 'alt-calc-popup';
  popup.style.cssText = 'position:fixed;top:60px;right:16px;z-index:9999;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 16px;min-width:240px;box-shadow:0 4px 24px rgba(0,0,0,0.3);font-size:12px';
  popup.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <b style="font-size:13px">🔭 Высота и GSD</b>
      <button onclick="document.getElementById('alt-calc-popup').remove()" style="background:none;border:none;cursor:pointer;font-size:16px;color:var(--text2);line-height:1">×</button>
    </div>
    <label style="margin-bottom:6px">БВС
      <select id="ac-uav" style="font-size:11px">${uavOpts}</select>
    </label>
    <label style="margin-bottom:6px">Целевой GSD (см/пкс)
      <div style="display:flex;gap:6px;align-items:center">
        <input id="ac-gsd" type="number" value="3" min="0.5" max="50" step="0.5" style="flex:1;font-size:12px" />
        <span id="ac-gsd-class" style="font-size:10px;color:var(--accent);white-space:nowrap">ГИС</span>
      </div>
    </label>
    <label style="margin-bottom:8px">Высота AGL (м)
      <div style="display:flex;gap:6px;align-items:center">
        <input id="ac-alt" type="number" value="150" min="20" max="4000" step="5" style="flex:1;font-size:12px" />
        <span id="ac-gsd-out" style="font-size:10px;color:var(--text2);white-space:nowrap">GSD: ?</span>
      </div>
    </label>
    <div id="ac-result" style="font-size:11px;padding:6px 8px;background:var(--surface2);border-radius:6px;margin-bottom:8px"></div>
    <button id="ac-apply" class="btn btn-primary btn-sm" style="width:100%;margin-bottom:8px">✅ Применить высоту</button>
    <div style="font-size:10px;color:var(--text2);margin-bottom:4px">Справка по высотам:</div>
    <table id="ac-sweep" style="width:100%;border-collapse:collapse;font-size:10px">
      <thead><tr style="color:var(--text2)"><th style="text-align:left;padding:2px 4px">Высота</th><th style="padding:2px 4px">GSD</th><th style="padding:2px 4px">Полоса</th><th style="padding:2px 4px">Класс</th></tr></thead>
      <tbody id="ac-sweep-body"></tbody>
    </table>
  `;
  document.body.appendChild(popup);

  function _calcGsd() {
    const uav = state.uavTypes.find(u => u.id === document.getElementById('ac-uav').value);
    const alt = parseFloat(document.getElementById('ac-alt').value) || 150;
    if (!uav) return;
    const payloadId = document.getElementById('payload-type')?.value || 'rgb';
    const pixelUm = (state.payloadSpecs?.[payloadId]?.pixel_um) || 4.51;
    const fmm = uav.focal_mm || 35;
    const gsd_cm = pixelUm * alt / fmm / 10;
    document.getElementById('ac-gsd-out').textContent = `GSD: ${gsd_cm.toFixed(1)} см`;
    const cls = gsd_cm <= 2 ? '🏆 Кадастр' : gsd_cm <= 5 ? '✅ ГИС/ортофото' : gsd_cm <= 10 ? '📊 Мониторинг' : '🔍 Обзорная';
    const swath = (uav.sensor_w_mm || 35.9) / fmm * alt;
    document.getElementById('ac-result').innerHTML =
      `GSD: <b>${gsd_cm.toFixed(2)} см/пкс</b> · Класс: <b>${cls}</b><br/>Полоса захвата: <b>${swath.toFixed(0)} м</b>`;
    // Sweep table
    const tbody = document.getElementById('ac-sweep-body');
    if (tbody) {
      const sweepAlts = [50, 75, 100, 150, 200, 300, 500];
      tbody.innerHTML = sweepAlts.map(h => {
        const g = pixelUm * h / fmm / 10;
        const sw = (uav.sensor_w_mm || 35.9) / fmm * h;
        const cl = g <= 2 ? '🏆' : g <= 5 ? '✅' : g <= 10 ? '📊' : '🔍';
        const isActive = Math.abs(h - alt) < 10;
        const rowStyle = isActive ? 'background:var(--accent)22;font-weight:600' : '';
        return `<tr style="${rowStyle}">
          <td style="padding:2px 4px">${h} м</td>
          <td style="padding:2px 4px;text-align:center">${g.toFixed(1)} см</td>
          <td style="padding:2px 4px;text-align:center">${sw.toFixed(0)} м</td>
          <td style="padding:2px 4px;text-align:center">${cl}</td>
        </tr>`;
      }).join('');
    }
    return gsd_cm;
  }

  function _calcAlt() {
    const uav = state.uavTypes.find(u => u.id === document.getElementById('ac-uav').value);
    const gsd = parseFloat(document.getElementById('ac-gsd').value) || 3;
    if (!uav) return;
    const payloadId = document.getElementById('payload-type')?.value || 'rgb';
    const pixelUm = (state.payloadSpecs?.[payloadId]?.pixel_um) || 4.51;
    const fmm = uav.focal_mm || 35;
    const alt = gsd * fmm * 10 / pixelUm;
    document.getElementById('ac-alt').value = Math.round(alt);
    const cls = gsd <= 2 ? '🏆 Кадастр' : gsd <= 5 ? '✅ ГИС/ортофото' : gsd <= 10 ? '📊 Мониторинг' : '🔍 Обзорная';
    document.getElementById('ac-gsd-class').textContent = cls;
    _calcGsd();
  }

  document.getElementById('ac-gsd').addEventListener('input', _calcAlt);
  document.getElementById('ac-alt').addEventListener('input', _calcGsd);
  document.getElementById('ac-uav').addEventListener('change', _calcGsd);
  document.getElementById('ac-apply').addEventListener('click', () => {
    const alt = document.getElementById('ac-alt').value;
    document.getElementById('altitude').value = alt;
    popup.remove();
    updateAreaInfo();
    setStatus(`Высота задана: ${alt} м`, 'ok');
  });
  _calcGsd();
}

// ─── Live weather fetch (Open-Meteo, free/no-key) ────────────────────────────
async function fetchWeather() {
  let lat, lon;
  // Try center of drawn area first, fallback to map center
  if (state.areaPolygons.length) {
    const pts = state.areaPolygons.flatMap(l => l.getLatLngs()[0] || []);
    lat = pts.reduce((s, p) => s + p.lat, 0) / pts.length;
    lon = pts.reduce((s, p) => s + p.lng, 0) / pts.length;
  } else {
    const c = map.getCenter();
    lat = c.lat; lon = c.lng;
  }
  setStatus('⟳ Загрузка погоды...', 'loading');
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat.toFixed(4)}&longitude=${lon.toFixed(4)}&current=wind_speed_10m,wind_direction_10m,wind_gusts_10m,temperature_2m,precipitation,cloud_cover,visibility&hourly=wind_speed_10m,wind_gusts_10m,precipitation,cloud_cover&forecast_days=2&wind_speed_unit=ms&timezone=auto`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const c = data.current;
    const ws = c.wind_speed_10m ?? 0;
    const wd = c.wind_direction_10m ?? 0;
    const wg = c.wind_gusts_10m ?? 0;
    const temp = c.temperature_2m ?? '?';
    const cloud = c.cloud_cover ?? '?';
    const vis = c.visibility != null ? (c.visibility / 1000).toFixed(1) : '?';
    const prec = c.precipitation ?? 0;
    // Auto-fill wind inputs
    document.getElementById('wind-speed').value = ws.toFixed(1);
    document.getElementById('wind-dir').value = Math.round(wd);
    document.getElementById('wind-speed').dispatchEvent(new Event('input'));

    // Find best 4-hour launch window in next 48 h (max UAV wind limit)
    const maxUavWind = Math.min(...(state.uavRows || []).map(r => {
      const spec = state.uavTypes.find(t => t.id === r.typeId);
      return spec?.max_wind_ms ?? 12;
    }).filter(v => v > 0), 12);
    const hTimes = data.hourly?.time || [];
    const hWind = data.hourly?.wind_speed_10m || [];
    const hGusts = data.hourly?.wind_gusts_10m || [];
    const hPrec = data.hourly?.precipitation || [];
    const hCloud = data.hourly?.cloud_cover || [];
    const now = Date.now();
    // Score each 4-hour window starting from current hour
    let bestWindow = null, bestScore = Infinity;
    for (let i = 0; i < hTimes.length - 4; i++) {
      const t = new Date(hTimes[i]).getTime();
      if (t < now - 3600000) continue;
      const windAvg = (hWind[i]+hWind[i+1]+hWind[i+2]+hWind[i+3]) / 4;
      const gustMax = Math.max(hGusts[i], hGusts[i+1], hGusts[i+2], hGusts[i+3]);
      const precSum = hPrec[i]+hPrec[i+1]+hPrec[i+2]+hPrec[i+3];
      const score = windAvg * 2 + gustMax + precSum * 10;
      if (score < bestScore && gustMax <= maxUavWind) { bestScore = score; bestWindow = i; }
    }
    const windowHtml = bestWindow != null ? (() => {
      const wStart = new Date(hTimes[bestWindow]);
      const wEnd = new Date(hTimes[bestWindow + 3]);
      const wAvg = ((hWind[bestWindow]+hWind[bestWindow+1]+hWind[bestWindow+2]+hWind[bestWindow+3])/4).toFixed(1);
      const wDay = wStart.toLocaleDateString('ru-RU', {weekday:'short', day:'numeric', month:'short'});
      const wFrom = wStart.toLocaleTimeString('ru-RU', {hour:'2-digit', minute:'2-digit'});
      const wTo = wEnd.toLocaleTimeString('ru-RU', {hour:'2-digit', minute:'2-digit'});
      const wHH = String(wStart.getHours()).padStart(2,'0');
      const wMM = String(wStart.getMinutes()).padStart(2,'0');
      return `<div style="padding:6px 8px;background:#10b98122;border-radius:6px;margin-top:6px">
        <div style="font-size:10px;font-weight:700;color:#10b981;margin-bottom:2px">🕐 Лучшее окно для вылета</div>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div>
            <div style="font-size:11px"><b>${wDay} ${wFrom}–${wTo}</b></div>
            <div style="font-size:10px;color:var(--text2)">Ветер ≈ ${wAvg} м/с</div>
          </div>
          <button id="weather-apply-window" class="btn btn-secondary btn-sm" style="font-size:10px;padding:3px 8px">Применить</button>
        </div>
      </div>`;
    })() : '';

    // Hourly mini bar chart (next 12 hours)
    const hoursToShow = 12;
    const nowIdx = hTimes.findIndex(t => new Date(t).getTime() >= now - 1800000);
    const chartSlice = hTimes.slice(nowIdx, nowIdx + hoursToShow);
    const windSlice = hWind.slice(nowIdx, nowIdx + hoursToShow);
    const gustSlice = hGusts.slice(nowIdx, nowIdx + hoursToShow);
    const precSlice = hPrec.slice(nowIdx, nowIdx + hoursToShow);
    const maxW = Math.max(...windSlice, maxUavWind, 5);
    const barW = 100 / hoursToShow;
    const barsHtml = chartSlice.map((t, i) => {
      const h = new Date(t).getHours();
      const w = windSlice[i] || 0;
      const g = gustSlice[i] || 0;
      const p = precSlice[i] || 0;
      const barH = Math.round(w / maxW * 28);
      const gustH = Math.round(g / maxW * 28);
      const clr = w > maxUavWind ? '#ef4444' : w > maxUavWind * 0.8 ? '#f59e0b' : '#10b981';
      const rain = p > 0 ? `<div style="position:absolute;bottom:0;left:0;right:0;height:${Math.min(p*4,8)}px;background:#60a5fa44"></div>` : '';
      return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;position:relative" title="${h}:00 ветер ${w.toFixed(1)} м/с, порывы ${g.toFixed(1)}">
        <div style="position:relative;width:100%;height:30px;display:flex;align-items:flex-end;justify-content:center">
          <div style="position:absolute;bottom:0;left:20%;right:20%;height:${gustH}px;background:${clr}33;border-radius:1px"></div>
          <div style="position:absolute;bottom:0;left:25%;right:25%;height:${barH}px;background:${clr};border-radius:1px">${rain}</div>
        </div>
        <div style="font-size:7px;color:var(--text2);margin-top:1px">${h}</div>
      </div>`;
    }).join('');
    const limitLineY = Math.round((1 - maxUavWind / maxW) * 28);
    const chartHtml = `<div style="margin-top:8px">
      <div style="font-size:10px;color:var(--text2);margin-bottom:3px">Ветер след. 12 ч (м/с) <span style="color:#ef4444">— лимит БВС ${maxUavWind} м/с</span></div>
      <div style="position:relative">
        <div style="display:flex;gap:1px;align-items:flex-end">${barsHtml}</div>
        <div style="position:absolute;top:${limitLineY}px;left:0;right:0;height:1px;background:#ef444488;pointer-events:none"></div>
      </div>
    </div>`;

    // Show weather info popup
    const flyOk = ws <= maxUavWind && prec === 0 && (c.visibility == null || c.visibility >= 1000);
    const flyColor = flyOk ? '#10b981' : '#ef4444';
    const flyText = flyOk ? '✅ Условия благоприятны' : `⚠ Ветер ${ws} м/с (лимит ${maxUavWind} м/с)`;
    const popup = document.createElement('div');
    popup.id = 'weather-popup';
    popup.style.cssText = 'position:fixed;top:60px;right:16px;z-index:9999;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 16px;width:260px;box-shadow:0 4px 24px rgba(0,0,0,0.3);font-size:12px;max-height:80vh;overflow-y:auto';
    popup.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <b style="font-size:13px">🌤 Погода в районе миссии</b>
        <button onclick="document.getElementById('weather-popup').remove()" style="background:none;border:none;cursor:pointer;font-size:16px;color:var(--text2);line-height:1">×</button>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;margin-bottom:8px">
        <span style="color:var(--text2)">Ветер</span><span><b>${ws} м/с</b> (${Math.round(wd)}°)</span>
        <span style="color:var(--text2)">Порывы</span><span>${wg} м/с</span>
        <span style="color:var(--text2)">Температура</span><span>${temp} °C</span>
        <span style="color:var(--text2)">Облачность</span><span>${cloud}%</span>
        <span style="color:var(--text2)">Видимость</span><span>${vis} км</span>
        <span style="color:var(--text2)">Осадки</span><span>${prec} мм/ч</span>
      </div>
      <div style="padding:5px 8px;background:${flyColor}22;border-radius:6px;color:${flyColor};font-weight:600;font-size:11px">${flyText}</div>
      ${windowHtml}
      ${chartHtml}
      <div style="font-size:10px;color:var(--text2);margin-top:6px">Данные: Open-Meteo · ${new Date().toLocaleTimeString('ru-RU')}</div>
    `;
    document.getElementById('weather-popup')?.remove();
    document.body.appendChild(popup);
    if (bestWindow != null) {
      const wStart2 = new Date(hTimes[bestWindow]);
      document.getElementById('weather-apply-window')?.addEventListener('click', () => {
        const hh = String(wStart2.getHours()).padStart(2,'0');
        const mm = String(wStart2.getMinutes()).padStart(2,'0');
        const dep = document.getElementById('departure-time');
        if (dep) dep.value = `${hh}:${mm}`;
        popup.remove();
        setStatus(`🕐 Время вылета установлено на ${hh}:${mm}`, 'ok');
      });
    }
    setStatus(`🌤 Ветер ${ws} м/с / ${Math.round(wd)}° — данные обновлены`, 'ok');
  } catch (e) {
    setStatus(`Ошибка загрузки погоды: ${e.message}`, 'error');
  }
}

function generateMissionReport(missions, summary) {
  if (!missions || !summary) return;
  const now = new Date().toLocaleString('ru-RU');
  const dv = document.getElementById('departure-time')?.value || '09:00';
  const [_dh, _dm] = dv.split(':').map(Number);
  const _baseMin = _dh * 60 + _dm;
  const windSpeed = parseFloat(document.getElementById('wind-speed')?.value || '0');
  const windDir = document.getElementById('wind-dir')?.value || '0';
  const altitude = document.getElementById('altitude')?.value || '?';
  const payloadType = document.getElementById('payload-type')?.options[document.getElementById('payload-type')?.selectedIndex]?.text || '?';
  const overlapSide = document.getElementById('overlap-side')?.value || '?';
  const overlapFront = document.getElementById('overlap-front')?.value || '?';
  const rows = (summary.missions || []).map((m, i) => {
    const wps = (missions[i]?.waypoints || []).filter(w => ['takeoff','climb','cruise','survey_start','survey_end','rtl','land'].includes(w.action));
    let pts = [], dist = 0;
    const ER = 6371000;
    for (let j = 0; j < wps.length; j++) {
      if (j > 0) {
        const a = wps[j-1], b = wps[j];
        const dlat = (b.lat - a.lat) * Math.PI/180;
        const dlon = (b.lon - a.lon) * Math.PI/180;
        const mlat = (a.lat + b.lat)/2 * Math.PI/180;
        dist += Math.sqrt((dlat*ER)**2 + (dlon*ER*Math.cos(mlat))**2);
      }
      pts.push({ d: dist, alt: wps[j].alt_m || 0 });
    }
    let svgStr = '';
    if (pts.length > 1) {
      const W=300, H=60;
      const maxD = pts[pts.length-1].d || 1;
      const maxA = Math.max(...pts.map(p=>p.alt))*1.15||200;
      const tx = d => Math.round(d/maxD*W);
      const ty = a => Math.round(H - a/maxA*H);
      const fill = pts.map((p,k) => k===0?`M${tx(p.d)},${ty(p.alt)}`:`L${tx(p.d)},${ty(p.alt)}`).join(' ') + ` L${W},${H} L0,${H} Z`;
      const line = pts.map(p=>`${tx(p.d)},${ty(p.alt)}`).join(' ');
      svgStr = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="background:#f1f5f9;border-radius:4px;display:block;margin:6px 0"><path d="${fill}" fill="rgba(59,130,246,0.2)"/><polyline points="${line}" fill="none" stroke="#3b82f6" stroke-width="2"/></svg>`;
    }
    const warn = m.cruise_count > 0 ? `⚡ Обход БЗ (${m.cruise_count} тч.)` : '';
    const landMin = _baseMin + Math.round(m.time_min);
    const landH = Math.floor(landMin / 60) % 24, landM = landMin % 60;
    const timeStr = `${dv} → ${String(landH).padStart(2,'0')}:${String(landM).padStart(2,'0')}`;
    const wfPct = m.wind_power_factor && m.wind_power_factor > 1.01 ? ` (+${Math.round((m.wind_power_factor-1)*100)}% ветер)` : '';
    return `<tr><td>${ROUTE_COLORS[i%ROUTE_COLORS.length]?`<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${ROUTE_COLORS[i%ROUTE_COLORS.length]}"></span> `:''}<b>${m.uav}</b></td><td>${m.distance_km} км</td><td>${m.time_min} мин${wfPct}</td><td>${timeStr}</td><td>${m.area_km2 || '—'} км²</td><td>${m.gsd_cm || '—'} см</td><td>${m.strip_count}</td><td>${m.photo_count}</td><td>${m.survey_pct || 0}%</td><td>${warn}</td></tr><tr><td colspan="10">${svgStr}<small style="color:#64748b">Профиль высоты маршрута | Взлёт: ${_takeoffLabel(m.takeoff_type)} | Посадка: ${_landLabel(m.landing_type)}</small></td></tr>`;
  }).join('');

  const totalCost = (summary.missions||[]).reduce((s,m)=>s+(m.cost_rub_est||0),0);
  const gcpRows = (state.gcpMarkers || []).map((m, i) => {
    const ll = m.getLatLng();
    return `<tr><td>ГКТ ${i+1}</td><td>${ll.lat.toFixed(6)}</td><td>${ll.lng.toFixed(6)}</td><td>На земле</td></tr>`;
  }).join('');
  const gcpSection = gcpRows ? `<h3>Наземные контрольные точки (ГКТ)</h3><table><thead><tr><th>Точка</th><th>Широта</th><th>Долгота</th><th>Метод определения</th></tr></thead><tbody>${gcpRows}</tbody></table>` : '';
  const dataGB = (summary.total_photos * 15 / 1024).toFixed(1);
  const uploadMin = Math.ceil(summary.total_photos * 15 / (100 * 1024 / 8) / 60);
  // Feasibility scores for report
  const feasRows = (summary.missions || []).map((m, i) => {
    const spec = state.uavTypes.find(t => t.id === m.uav_id);
    const maxTime = spec?.max_flight_time_min || null;
    const bPct = maxTime ? Math.round(m.time_min / maxTime * 100 * (m.wind_power_factor || 1)) : null;
    const _b = bPct != null ? Math.max(0, Math.min(100, 120 - bPct)) : 70;
    const _s = m.survey_pct || 70;
    const _n = m.cruise_count > 0 ? 70 : 100;
    const _g = m.gsd_cm ? (m.gsd_cm <= 2 ? 100 : m.gsd_cm <= 5 ? 85 : m.gsd_cm <= 10 ? 65 : 40) : 75;
    const fs = Math.round(_b*0.4 + _s*0.3 + _n*0.15 + _g*0.15);
    const fc = fs >= 80 ? '#16a34a' : fs >= 60 ? '#d97706' : '#dc2626';
    const fl = fs >= 80 ? 'Отлично' : fs >= 60 ? 'Пригоден' : 'Риск';
    return `<tr><td><b>${m.uav}</b></td><td style="color:${fc};font-weight:700">${fs} — ${fl}</td><td>${bPct != null ? bPct+'%' : '—'}</td><td>${m.survey_pct || '—'}%</td><td>${m.gsd_cm || '—'} см</td><td>${m.cruise_count > 0 ? '⚠ Да' : '✅ Нет'}</td></tr>`;
  }).join('');
  // Wind analysis table for report
  const windSpeeds = [0, 5, 10, 15];
  const windAnalysisRows = (summary.missions || []).map(m => {
    const spec = state.uavTypes.find(t => t.id === m.uav_id);
    if (!spec) return '';
    const v = spec.cruise_speed_ms;
    const cells = windSpeeds.map(w => {
      let wpf = 1.0;
      if (w > 0 && v > 0) { const vh=v+w,vt=Math.max(v-w,1); wpf=((vh**2.5+vt**2.5)/2)/(v**2.5); }
      const bp = Math.round(m.time_min / spec.max_flight_time_min * 100 * wpf);
      const clr = bp > 100 ? '#dc2626' : bp > 85 ? '#d97706' : '#16a34a';
      return `<td style="text-align:center;color:${clr};font-weight:${bp>85?'700':'400'}">${bp}%${w > spec.max_wind_ms ? '<br/><span style="font-size:9px">⛔</span>' : ''}</td>`;
    }).join('');
    return `<tr><td><b>${m.uav}</b></td>${cells}</tr>`;
  }).join('');
  const terrain = state._terrainData;
  const terrainSection = terrain ? `
<h3>Оценка рельефа</h3>
<dl class="params-grid">
  <div><dt>Рельеф (мин.)</dt><dd>${Math.round(terrain.minElev)} м над ур.м.</dd></div>
  <div><dt>Рельеф (макс.)</dt><dd>${Math.round(terrain.maxElev)} м над ур.м.</dd></div>
  <div><dt>Перепад высот</dt><dd>${Math.round(terrain.relief)} м</dd></div>
  <div><dt>Высота ВПП (AMSL)</dt><dd>~${Math.round(terrain.vppElev)} м</dd></div>
  <div><dt>Высота дрона (AMSL)</dt><dd>~${Math.round(terrain.vppElev + parseFloat(altitude))} м</dd></div>
  <div><dt>Клиренс над рельефом</dt><dd style="color:${terrain.clearance < 30 ? '#dc2626' : terrain.clearance < 80 ? '#d97706' : '#16a34a'};font-weight:700">${Math.round(terrain.clearance)} м ${terrain.clearance < 30 ? '⚠ КРИТИЧНО' : terrain.clearance < 80 ? '⚠ Мало' : '✅ OK'}</dd></div>
</dl>` : '';
  const html = `<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><title>Отчёт о полётном задании — Geoscan UAV Planner</title>
<style>
body{font-family:system-ui,sans-serif;padding:24px 32px;color:#0f172a;max-width:960px;margin:0 auto}
h1{color:#1e3a5f;margin-bottom:4px}h2{font-size:14px;color:#475569;margin-top:0;margin-bottom:16px}
h3{font-size:13px;font-weight:700;color:#334155;margin:20px 0 8px;border-bottom:1px solid #e2e8f0;padding-bottom:4px}
table{border-collapse:collapse;width:100%;font-size:12px;margin-top:8px}
th,td{border:1px solid #e2e8f0;padding:6px 10px;text-align:left}
th{background:#f1f5f9;font-weight:600}tr:hover td{background:#f8fafc}
.kpi-row{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}
.kpi{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 14px;text-align:center;min-width:80px}
.kpi-val{display:block;font-size:20px;font-weight:700;color:#1e3a5f}
.kpi-lbl{font-size:11px;color:#64748b}
.params-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px 16px;font-size:12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px 16px;margin:8px 0}
.params-grid dt{color:#64748b;font-size:11px}
.params-grid dd{color:#0f172a;font-weight:600;margin:0}
.print-btn{float:right;background:#1e3a5f;color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:12px;cursor:pointer}
.print-btn:hover{background:#2563eb}
.note{margin-top:20px;font-size:11px;color:#94a3b8;border-top:1px solid #e2e8f0;padding-top:12px}
@media print{.print-btn{display:none}body{padding:12px}}
</style>
</head><body>
<button class="print-btn" onclick="window.print()">🖨 Печать / PDF</button>
<h1>Отчёт о полётном задании</h1>
<h2>Geoscan UAV Planner · Сформирован: ${now}</h2>
<div class="kpi-row">
  <div class="kpi"><span class="kpi-val">${summary.total_uavs}</span><span class="kpi-lbl">БВС</span></div>
  <div class="kpi"><span class="kpi-val">${summary.total_area_km2?.toFixed(2)}</span><span class="kpi-lbl">км² покрыто</span></div>
  <div class="kpi"><span class="kpi-val">${summary.max_mission_time_min?.toFixed(0)}</span><span class="kpi-lbl">мин макс.</span></div>
  <div class="kpi"><span class="kpi-val">${summary.total_distance_km?.toFixed(1)}</span><span class="kpi-lbl">км суммарно</span></div>
  <div class="kpi"><span class="kpi-val">${summary.total_photos > 999 ? (summary.total_photos/1000).toFixed(1)+'k' : summary.total_photos}</span><span class="kpi-lbl">снимков</span></div>
  <div class="kpi"><span class="kpi-val">${dataGB}</span><span class="kpi-lbl">ГБ данных</span></div>
  ${totalCost > 0 ? `<div class="kpi"><span class="kpi-val">${Math.round(totalCost/1000)}</span><span class="kpi-lbl">тыс. ₽</span></div>` : ''}
</div>
<h3>Параметры полёта</h3>
<dl class="params-grid">
  <div><dt>Высота AGL</dt><dd>${altitude} м</dd></div>
  <div><dt>Тип съёмки</dt><dd>${payloadType}</dd></div>
  <div><dt>Перекрытие бок./прод.</dt><dd>${overlapSide}% / ${overlapFront}%</dd></div>
  <div><dt>Ветер</dt><dd>${windSpeed} м/с, направление ${windDir}°</dd></div>
  <div><dt>Время вылета</dt><dd>${dv}</dd></div>
  <div><dt>Расчётная загрузка</dt><dd>${dataGB} ГБ (~${uploadMin} мин загрузки)</dd></div>
</dl>
<h3>Маршруты БВС</h3>
<table><thead><tr><th>БВС</th><th>Дистанция</th><th>Время</th><th>Вылет / Посадка</th><th>Площадь</th><th>GSD</th><th>Маршруты</th><th>Снимков</th><th>КПД</th><th>Особое</th></tr></thead><tbody>${rows}</tbody></table>
${feasRows ? `<h3>Оценка пригодности маршрутов</h3>
<table><thead><tr><th>БВС</th><th>Итог (0–100)</th><th>Батарея %</th><th>КПД съёмки</th><th>GSD</th><th>Обход БЗ</th></tr></thead><tbody>${feasRows}</tbody></table>` : ''}
${windAnalysisRows ? `<h3>Анализ ветровой нагрузки (% расхода заряда)</h3>
<table><thead><tr><th>БВС</th>${windSpeeds.map(w=>`<th>${w} м/с</th>`).join('')}</tr></thead><tbody>${windAnalysisRows}</tbody></table>
<p style="font-size:11px;color:#64748b">⛔ — скорость ветра превышает допустимую для данного БВС</p>` : ''}
${terrainSection}
${gcpSection}
<p class="note">Сгенерировано: Geoscan UAV Planner (ЛЦТ 2026) · Данные носят оценочный характер</p>
</body></html>`;
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  downloadBlob(blob, 'mission_report.html');
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

// ─── MAVLink .waypoints export ────────────────────────────────────────────────
function exportMAVLink(missions) {
  if (!missions || !missions.length) return;
  const ACTION_CMD = { takeoff: 22, climb: 16, survey_start: 16, survey_end: 16, cruise: 16, rtl: 20, land: 21 };
  let lines = ['QGC WPL 110'];
  let idx = 0;
  missions.forEach(m => {
    const wps = (m.waypoints || []).filter(w => w.action !== 'photo');
    wps.forEach((wp, wi) => {
      const cmd = ACTION_CMD[wp.action] || 16;
      const cur = idx === 0 ? 1 : 0;
      const p1 = wp.action === 'takeoff' ? (wp.alt_m || 0) : 0;
      lines.push([idx, cur, 3, cmd, p1, 0, 0, 0,
        wp.lat.toFixed(8), wp.lon.toFixed(8), (wp.alt_m || 0).toFixed(2), 1].join('\t'));
      idx++;
    });
  });
  const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
  downloadBlob(blob, 'flight_plan.waypoints');
}

// ─── Payload info card ────────────────────────────────────────────────────────
function renderPayloadInfo(payloadId) {
  const el = document.getElementById('payload-info');
  if (!el) return;
  const p = state.payloadSpecs[payloadId];
  if (!p) { el.style.display = 'none'; return; }
  el.style.display = '';
  el.innerHTML = `
    <div class="spec-card">
      <div class="spec-card-title">${p.name}</div>
      <div class="spec-grid">
        <span class="spec-key">Сенсор</span><span class="spec-val">${p.camera}</span>
        ${p.resolution_mp ? `<span class="spec-key">Разрешение</span><span class="spec-val">${p.resolution_mp} МП</span>` : ''}
        ${p.focal_mm ? `<span class="spec-key">Фокус</span><span class="spec-val">${p.focal_mm} мм</span>` : ''}
        <span class="spec-key">Матрица</span><span class="spec-val">${p.sensor_mm}</span>
        <span class="spec-key">Спектр / каналы</span><span class="spec-val">${p.bands}</span>
        ${p.gsd_150m_cm ? `<span class="spec-key">GSD @ 150 м</span><span class="spec-val">${p.gsd_150m_cm} см/пкс</span>` : ''}
        <span class="spec-key">Примечание</span><span class="spec-val">${p.notes}</span>
      </div>
    </div>
  `;
}

// ─── Fleet reference table ─────────────────────────────────────────────────────
function renderFleetRef() {
  const el = document.getElementById('fleet-ref-body');
  if (!el || !state.uavTypes.length) return;
  el.innerHTML = state.uavTypes.map(t => `
    <tr>
      <td><b>${t.name}</b></td>
      <td>${t.type === 'fixed_wing' ? 'Самолёт' : 'Мультиротор'}</td>
      <td>${t.max_flight_time_min} мин</td>
      <td>${Math.round(t.cruise_speed_ms * 3.6)} км/ч</td>
      <td>${t.max_wind_ms} м/с</td>
      <td>${t.max_altitude_agl_m} м</td>
      <td>${t.takeoff_type === 'catapult' ? 'Катапульта' : 'ВТОЛ'} / ${t.landing_type === 'parachute' ? 'Парашют' : 'ВТОЛ'}</td>
      <td>${t.supported_payloads.join(', ')}</td>
    </tr>
  `).join('');
}

// ─── Save / Load scenario ────────────────────────────────────────────────────
function saveScenario() {
  const nfzLayers = [...drawnItems.getLayers()].filter(l => l._layerType === 'nfz');
  const scenario = {
    version: 2,
    params: {
      altitude_m: +document.getElementById('altitude').value,
      payload_type: document.getElementById('payload-type').value,
      overlap_side: +document.getElementById('overlap-side').value,
      overlap_front: +document.getElementById('overlap-front').value,
      wind_speed_ms: +document.getElementById('wind-speed').value,
      wind_dir_deg: +document.getElementById('wind-dir').value,
      optimization: document.getElementById('optimization').value,
    },
    area_polygons: state.areaPolygons.map(l => l.getLatLngs()[0].map(ll => [ll.lat, ll.lng])),
    area_polygon: state.areaPolygon
      ? state.areaPolygon.getLatLngs()[0].map(ll => [ll.lat, ll.lng]) : null,
    airspace_boundary: state.airspaceBoundary
      ? state.airspaceBoundary.getLatLngs()[0].map(ll => [ll.lat, ll.lng]) : null,
    no_fly_zones: nfzLayers.map(l => l.getLatLngs()[0].map(ll => [ll.lat, ll.lng])),
    landing_sites: state.siteMarkers.map(s => ({ id: s.id, latlon: s.latlon })),
    reserve_landing_areas: state.reserveMarkers.map(m => [m.getLatLng().lat, m.getLatLng().lng]),
    uavs: state.uavRows.map(r => ({
      typeId: r.typeId,
      siteId: r.siteId || null,
      startLatLon: r.startLatLon || null,
    })),
  };
  const blob = new Blob([JSON.stringify(scenario, null, 2)], { type: 'application/json' });
  downloadBlob(blob, 'scenario.json');
  setStatus('Сценарий сохранён', 'ok');
}

function loadScenario(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const sc = JSON.parse(e.target.result);
      clearAll();

      // Restore params
      if (sc.params) {
        const p = sc.params;
        if (p.altitude_m != null) document.getElementById('altitude').value = p.altitude_m;
        if (p.payload_type) document.getElementById('payload-type').value = p.payload_type;
        if (p.overlap_side != null) document.getElementById('overlap-side').value = p.overlap_side;
        if (p.overlap_front != null) document.getElementById('overlap-front').value = p.overlap_front;
        if (p.wind_speed_ms != null) document.getElementById('wind-speed').value = p.wind_speed_ms;
        if (p.wind_dir_deg != null) document.getElementById('wind-dir').value = p.wind_dir_deg;
        if (p.optimization) document.getElementById('optimization').value = p.optimization;
        renderPayloadInfo(document.getElementById('payload-type').value);
      }

      // Restore area zones
      const zonesList = sc.area_polygons?.length >= 1
        ? sc.area_polygons
        : (sc.area_polygon?.length >= 3 ? [sc.area_polygon] : []);
      zonesList.forEach((coords, zoneIdx) => {
        if (coords.length < 3) return;
        const lls = coords.map(([lat, lon]) => L.latLng(lat, lon));
        const color = ROUTE_COLORS[zoneIdx % ROUTE_COLORS.length];
        const layer = L.polygon(lls, { color, fillOpacity: 0.15 });
        layer._layerType = 'area';
        layer._zoneIndex = zoneIdx;
        layer.bindTooltip(`Зона ${zoneIdx + 1}`, { permanent: true, direction: 'center', className: 'zone-label' });
        state.areaPolygons.push(layer);
        state.areaPolygon = layer;
        drawnItems.addLayer(layer);
      });

      // Restore airspace
      if (sc.airspace_boundary?.length >= 3) {
        const lls = sc.airspace_boundary.map(([lat, lon]) => L.latLng(lat, lon));
        const layer = L.polygon(lls, { color: '#a855f7', fillOpacity: 0.08, dashArray: '8,4' });
        layer._layerType = 'airspace';
        state.airspaceBoundary = layer;
        drawnItems.addLayer(layer);
      }

      // Restore NFZs
      (sc.no_fly_zones || []).forEach(coords => {
        if (coords.length < 3) return;
        const lls = coords.map(([lat, lon]) => L.latLng(lat, lon));
        const layer = L.polygon(lls, { color: '#ef4444', fillOpacity: 0.2, dashArray: '6,4', className: 'nfz-animated' });
        layer._layerType = 'nfz';
        drawnItems.addLayer(layer);
        _addNfzBuffer(layer);
      });

      // Restore landing sites
      (sc.landing_sites || []).forEach(s => {
        const [lat, lon] = s.latlon;
        const num = state.siteMarkers.length + 1;
        const m = L.marker([lat, lon], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#22c55e;width:16px;height:16px;border-radius:3px;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#000">${num}</div>`,
            iconSize: [16, 16], iconAnchor: [8, 8],
          }),
        }).addTo(map).bindPopup(`ВПП ${s.id}`);
        state.siteMarkers.push({ id: s.id, latlon: s.latlon, marker: m });
      });

      // Restore reserve areas
      (sc.reserve_landing_areas || []).forEach(([lat, lon]) => {
        const m = L.marker([lat, lon], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#f59e0b;width:14px;height:14px;border-radius:3px;border:2px solid #fff;transform:rotate(45deg)"></div>`,
            iconSize: [14, 14], iconAnchor: [7, 7],
          }),
        }).addTo(map).bindPopup(`Резервная площадка`);
        state.reserveMarkers.push(m);
      });

      // Restore UAV rows
      if (sc.uavs?.length) {
        state.uavRows = [];
        _uavCounter = 0;
        sc.uavs.forEach(u => {
          const id = ++_uavCounter;
          const siteId = u.siteId || null;
          const startLatLon = u.startLatLon || null;
          state.uavRows.push({ id, typeId: u.typeId || state.uavTypes[0]?.id, startLatLon, siteId, marker: null });
        });
        renderUAVRows();
      }

      updateAreaInfo();
      if (state.areaPolygons.length > 0) {
        try { map.fitBounds(drawnItems.getBounds().pad(0.15)); } catch {}
      }
      setStatus('Сценарий загружен', 'ok');
    } catch (err) {
      setStatus('Ошибка загрузки сценария: ' + err.message, 'error');
    }
  };
  reader.readAsText(file);
}

// ─── Auto-save / Auto-restore ────────────────────────────────────────────────
function copyShareLink() {
  try {
    const nfzLayers = [...drawnItems.getLayers()].filter(l => l._layerType === 'nfz');
    const sc = {
      version: 2,
      params: {
        altitude_m: +document.getElementById('altitude').value,
        payload_type: document.getElementById('payload-type').value,
        overlap_side: +document.getElementById('overlap-side').value,
        overlap_front: +document.getElementById('overlap-front').value,
        wind_speed_ms: +document.getElementById('wind-speed').value,
        wind_dir_deg: +document.getElementById('wind-dir').value,
        optimization: document.getElementById('optimization').value,
      },
      area_polygons: state.areaPolygons.map(l => l.getLatLngs()[0].map(ll => [ll.lat, ll.lng])),
      airspace_boundary: state.airspaceBoundary ? state.airspaceBoundary.getLatLngs()[0].map(ll => [ll.lat, ll.lng]) : null,
      no_fly_zones: nfzLayers.map(l => l.getLatLngs()[0].map(ll => [ll.lat, ll.lng])),
      landing_sites: state.siteMarkers.map(s => ({ id: s.id, latlon: s.latlon })),
      uavs: state.uavRows.map(r => ({ typeId: r.typeId, siteId: r.siteId || null })),
    };
    const encoded = btoa(unescape(encodeURIComponent(JSON.stringify(sc))));
    const url = `${location.origin}${location.pathname}#s=${encoded}`;
    navigator.clipboard?.writeText(url).then(() => {
      setStatus('📎 Ссылка на сценарий скопирована в буфер', 'ok');
    }).catch(() => {
      prompt('Скопируйте ссылку:', url);
    });
  } catch (e) {
    setStatus('Ошибка создания ссылки: ' + e.message, 'error');
  }
}

function checkShareHash() {
  try {
    const hash = location.hash;
    if (!hash.startsWith('#s=')) return;
    const encoded = hash.slice(3);
    const sc = JSON.parse(decodeURIComponent(escape(atob(encoded))));
    if (sc.version && (sc.area_polygons?.length || sc.area_polygon)) {
      setTimeout(() => {
        const file = new File([JSON.stringify(sc)], 'shared.json', { type: 'application/json' });
        loadScenario(file);
        setStatus('📎 Сценарий загружен из ссылки', 'ok');
        history.replaceState(null, '', location.pathname);
      }, 800);
    }
  } catch {}
}

function autoSaveScenario() {
  try {
    const nfzLayers = [...drawnItems.getLayers()].filter(l => l._layerType === 'nfz');
    const sc = {
      version: 2,
      _savedAt: new Date().toISOString(),
      params: {
        altitude_m: +document.getElementById('altitude').value,
        payload_type: document.getElementById('payload-type').value,
        overlap_side: +document.getElementById('overlap-side').value,
        overlap_front: +document.getElementById('overlap-front').value,
        wind_speed_ms: +document.getElementById('wind-speed').value,
        wind_dir_deg: +document.getElementById('wind-dir').value,
        optimization: document.getElementById('optimization').value,
      },
      area_polygons: state.areaPolygons.map(l => l.getLatLngs()[0].map(ll => [ll.lat, ll.lng])),
      area_polygon: state.areaPolygon ? state.areaPolygon.getLatLngs()[0].map(ll => [ll.lat, ll.lng]) : null,
      airspace_boundary: state.airspaceBoundary ? state.airspaceBoundary.getLatLngs()[0].map(ll => [ll.lat, ll.lng]) : null,
      no_fly_zones: nfzLayers.map(l => l.getLatLngs()[0].map(ll => [ll.lat, ll.lng])),
      landing_sites: state.siteMarkers.map(s => ({ id: s.id, latlon: s.latlon })),
      reserve_landing_areas: state.reserveMarkers.map(m => [m.getLatLng().lat, m.getLatLng().lng]),
      uavs: state.uavRows.map(r => ({ typeId: r.typeId, siteId: r.siteId || null, startLatLon: r.startLatLon || null })),
    };
    localStorage.setItem('geoscan_planner_autosave', JSON.stringify(sc));
  } catch {}
}

function checkAutoRestore() {
  try {
    const saved = localStorage.getItem('geoscan_planner_autosave');
    if (!saved) return;
    const sc = JSON.parse(saved);
    if (!sc._savedAt || !(sc.area_polygons?.length || sc.area_polygon)) return;
    const savedAt = new Date(sc._savedAt);
    const ageH = (Date.now() - savedAt.getTime()) / 3600000;
    if (ageH > 72) { localStorage.removeItem('geoscan_planner_autosave'); return; }
    const timeStr = savedAt.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    setStatus(`💾 Автосохранение ${timeStr}. <a href="#" id="_ar" style="color:#3b82f6;text-decoration:underline">Восстановить</a> &nbsp; <a href="#" id="_ar_skip" style="color:#94a3b8;font-size:10px">Скрыть</a>`, 'info');
    setTimeout(() => {
      document.getElementById('_ar')?.addEventListener('click', e => {
        e.preventDefault();
        const file = new File([JSON.stringify(sc)], 'autosave.json', { type: 'application/json' });
        loadScenario(file);
      });
      document.getElementById('_ar_skip')?.addEventListener('click', e => {
        e.preventDefault();
        document.getElementById('status-bar').innerHTML = '';
      });
    }, 100);
  } catch {}
}

// ─── GeoJSON import ──────────────────────────────────────────────────────────
function _applyGeoJSON(gj) {
  clearAll();
  const features = gj.type === 'FeatureCollection' ? gj.features
    : gj.type === 'Feature' ? [gj]
    : gj.type === 'Polygon' ? [{ type: 'Feature', geometry: gj, properties: { type: 'area' } }]
    : [];

  let areaSet = false;

  features.forEach(f => {
    const geomType = f.geometry?.type;
    const prop = (f.properties?.type || '').toLowerCase();
    const isPolygon = geomType === 'Polygon' || geomType === 'MultiPolygon';
    const isPoint = geomType === 'Point';
    const zoneType = prop || (isPolygon && !areaSet ? 'area' : prop);

    if (isPolygon) {
      const rings = geomType === 'Polygon' ? [f.geometry.coordinates[0]] : f.geometry.coordinates.map(r => r[0]);
      rings.forEach(ring => {
        const leafletLatLngs = ring.map(([lon, lat]) => L.latLng(lat, lon));
        if (zoneType === 'area' || (!prop && !areaSet)) {
          const zoneIdx = state.areaPolygons.length;
          const color = ROUTE_COLORS[zoneIdx % ROUTE_COLORS.length];
          const layer = L.polygon(leafletLatLngs, { color, fillOpacity: 0.15 });
          layer._layerType = 'area';
          layer._zoneIndex = zoneIdx;
          layer.bindTooltip(`Зона ${zoneIdx + 1}`, { permanent: true, direction: 'center', className: 'zone-label' });
          state.areaPolygons.push(layer);
          state.areaPolygon = layer;
          drawnItems.addLayer(layer);
          areaSet = true;
        } else if (zoneType === 'airspace') {
          const layer = L.polygon(leafletLatLngs, { color: '#a855f7', fillOpacity: 0.08, dashArray: '8,4' });
          layer._layerType = 'airspace';
          if (state.airspaceBoundary) drawnItems.removeLayer(state.airspaceBoundary);
          state.airspaceBoundary = layer;
          drawnItems.addLayer(layer);
        } else if (zoneType === 'no_fly_zone' || zoneType === 'nfz') {
          const layer = L.polygon(leafletLatLngs, { color: '#ef4444', fillOpacity: 0.2, dashArray: '6,4', className: 'nfz-animated' });
          layer._layerType = 'nfz';
          drawnItems.addLayer(layer);
          _addNfzBuffer(layer);
        }
      });
    } else if (isPoint) {
      const [lon, lat] = f.geometry.coordinates;
      if (zoneType === 'landing_site' || zoneType === 'site' || zoneType === 'vpp') {
        const siteId = f.properties?.id || `site_${state.siteMarkers.length + 1}`;
        const m = L.marker([lat, lon], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#22c55e;width:16px;height:16px;border-radius:3px;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#000">${state.siteMarkers.length + 1}</div>`,
            iconSize: [16, 16], iconAnchor: [8, 8],
          }),
        }).addTo(map).bindPopup(`ВПП ${siteId}: ${lat.toFixed(5)}, ${lon.toFixed(5)}`);
        state.siteMarkers.push({ id: siteId, latlon: [lat, lon], marker: m });
      } else if (zoneType === 'reserve_landing' || zoneType === 'reserve') {
        const m = L.marker([lat, lon], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#f59e0b;width:14px;height:14px;border-radius:3px;border:2px solid #fff;transform:rotate(45deg)"></div>`,
            iconSize: [14, 14], iconAnchor: [7, 7],
          }),
        }).addTo(map).bindPopup(`Резервная площадка: ${lat.toFixed(5)}, ${lon.toFixed(5)}`);
        state.reserveMarkers.push(m);
      }
    }
  });

  if (state.siteMarkers.length) renderUAVRows();
  updateAreaInfo();
  if (state.areaPolygons.length > 0) {
    try {
      const mainLayers = [...drawnItems.getLayers()].filter(l => l._layerType !== 'nfz-buffer');
      if (mainLayers.length) {
        const grp = L.featureGroup(mainLayers);
        map.fitBounds(grp.getBounds().pad(0.15));
      }
    } catch {}
  }
  return `Импортировано: ${features.length} объект(ов)`;
}

function importGeoJSON(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const gj = JSON.parse(e.target.result);
      const msg = _applyGeoJSON(gj);
      setStatus(msg, 'ok');
    } catch (err) {
      setStatus('Ошибка импорта GeoJSON: ' + err.message, 'error');
    }
  };
  reader.readAsText(file);
}

// ─── KML import ──────────────────────────────────────────────────────────────
function importKML(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const parser = new DOMParser();
      const xml = parser.parseFromString(e.target.result, 'text/xml');
      const placemarks = xml.querySelectorAll('Placemark');
      let imported = 0;
      placemarks.forEach(pm => {
        const name = pm.querySelector('name')?.textContent?.toLowerCase() || '';
        const coordsEl = pm.querySelector('Polygon coordinates, outerBoundaryIs coordinates');
        if (!coordsEl) return;
        const rawCoords = coordsEl.textContent.trim().split(/\s+/).map(s => {
          const parts = s.split(',');
          return [parseFloat(parts[1]), parseFloat(parts[0])]; // [lat, lon]
        }).filter(p => !isNaN(p[0]) && !isNaN(p[1]));
        if (rawCoords.length < 3) return;

        const leafletLatLngs = rawCoords.map(([lat, lon]) => L.latLng(lat, lon));
        let zoneType = 'area';
        if (name.includes('nfz') || name.includes('no_fly') || name.includes('запрет')) zoneType = 'nfz';
        else if (name.includes('airspace') || name.includes('вп')) zoneType = 'airspace';

        if (zoneType === 'area') {
          const zoneIdx = state.areaPolygons.length;
          const color = ROUTE_COLORS[zoneIdx % ROUTE_COLORS.length];
          const layer = L.polygon(leafletLatLngs, { color, fillOpacity: 0.15 });
          layer._layerType = 'area';
          layer._zoneIndex = zoneIdx;
          layer.bindTooltip(`Зона ${zoneIdx + 1}`, { permanent: true, direction: 'center', className: 'zone-label' });
          state.areaPolygons.push(layer);
          state.areaPolygon = layer;
          drawnItems.addLayer(layer);
        } else if (zoneType === 'airspace') {
          const layer = L.polygon(leafletLatLngs, { color: '#a855f7', fillOpacity: 0.08, dashArray: '8,4' });
          layer._layerType = 'airspace';
          if (state.airspaceBoundary) drawnItems.removeLayer(state.airspaceBoundary);
          state.airspaceBoundary = layer;
          drawnItems.addLayer(layer);
        } else {
          const layer = L.polygon(leafletLatLngs, { color: '#ef4444', fillOpacity: 0.2, dashArray: '6,4' });
          layer._layerType = 'nfz';
          drawnItems.addLayer(layer);
        }
        imported++;
      });
      updateAreaInfo();
      if (state.areaPolygons.length > 0) {
        try { map.fitBounds(drawnItems.getBounds().pad(0.15)); } catch {}
      }
      setStatus(`Импортировано из KML: ${imported} объект(ов)`, 'ok');
    } catch (err) {
      setStatus('Ошибка импорта KML: ' + err.message, 'error');
    }
  };
  reader.readAsText(file);
}

// ─── Bind extras ─────────────────────────────────────────────────────────────
function bindEvents() {
  document.getElementById('btn-add-uav').addEventListener('click', addUAVRow);

  document.getElementById('task-template')?.addEventListener('change', e => {
    const tpl = TASK_TEMPLATES[e.target.value];
    if (!tpl) return;
    if (tpl.altitude_m != null) document.getElementById('altitude').value = tpl.altitude_m;
    if (tpl.payload_type) { document.getElementById('payload-type').value = tpl.payload_type; renderPayloadInfo(tpl.payload_type); }
    if (tpl.overlap_side != null) document.getElementById('overlap-side').value = tpl.overlap_side;
    if (tpl.overlap_front != null) document.getElementById('overlap-front').value = tpl.overlap_front;
    renderUAVRows();
    updateAreaInfo();
  });
  document.getElementById('payload-type').addEventListener('change', e => {
    renderPayloadInfo(e.target.value);
    renderUAVRows();
    updateAreaInfo();
  });
  ['altitude', 'overlap-side', 'overlap-front'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', updateAreaInfo);
  });
  document.getElementById('fleet-ref-toggle').addEventListener('click', () => {
    const body = document.getElementById('fleet-ref-panel');
    const isHidden = body.style.display === 'none';
    body.style.display = isHidden ? '' : 'none';
    document.getElementById('fleet-ref-toggle').textContent = isHidden ? '▲ Свернуть' : '▼ Справочник БВС';
  });
  async function _loadDemoAndPlan(numUAVs) {
    setStatus('Загрузка демо…', 'loading');
    const r = await fetch('/demo.geojson?t=' + Date.now());
    const gj = await r.json();
    // Reset UAV rows so demo always starts fresh
    state.uavRows.forEach(row => { if (row.marker) map.removeLayer(row.marker); });
    state.uavRows = [];
    _uavCounter = 0;
    _applyGeoJSON(gj);
    for (let i = 0; i < numUAVs; i++) addUAVRow();
    if (state.siteMarkers.length > 0) {
      for (let i = 0; i < Math.min(numUAVs, state.siteMarkers.length); i++) {
        state.uavRows[i].siteId = state.siteMarkers[i].id;
      }
    }
    renderUAVRows();
    updateAreaInfo();
    setStatus('Демо загружено, вычисляем…', 'loading');
    document.getElementById('btn-plan').click();
  }

  document.getElementById('btn-load-demo').addEventListener('click', () => _loadDemoAndPlan(1));
  document.getElementById('btn-load-demo2').addEventListener('click', () => _loadDemoAndPlan(2));
  document.getElementById('btn-load-demo3').addEventListener('click', async () => {
    setStatus('Загрузка демо (смешанный парк)…', 'loading');
    const r = await fetch('/demo.geojson?t=' + Date.now());
    const gj = await r.json();
    state.uavRows.forEach(row => { if (row.marker) map.removeLayer(row.marker); });
    state.uavRows = [];
    _uavCounter = 0;
    _applyGeoJSON(gj);
    addUAVRow(); state.uavRows[0].typeId = 'geoscan_201';
    addUAVRow(); state.uavRows[1].typeId = 'geoscan_401';
    if (state.siteMarkers.length >= 2) {
      state.uavRows[0].siteId = state.siteMarkers[0].id;
      state.uavRows[1].siteId = state.siteMarkers[1].id;
    }
    renderUAVRows();
    updateAreaInfo();
    setStatus('Демо смешанный парк загружен, вычисляем…', 'loading');
    document.getElementById('btn-plan').click();
  });
  document.getElementById('btn-import-geojson').addEventListener('click', () => {
    document.getElementById('import-file').click();
  });
  document.getElementById('import-file').addEventListener('change', e => {
    if (e.target.files[0]) { importGeoJSON(e.target.files[0]); e.target.value = ''; }
  });
  document.getElementById('btn-import-kml').addEventListener('click', () => {
    document.getElementById('import-kml-file').click();
  });
  document.getElementById('import-kml-file').addEventListener('change', e => {
    if (e.target.files[0]) { importKML(e.target.files[0]); e.target.value = ''; }
  });

  // Startup cost slider
  const startupCostSlider = document.getElementById('startup-cost');
  const startupCostVal = document.getElementById('startup-cost-val');
  if (startupCostSlider && startupCostVal) {
    startupCostSlider.addEventListener('input', () => {
      startupCostVal.textContent = startupCostSlider.value;
    });
  }

  // Save / load scenario
  document.getElementById('btn-save-scenario').addEventListener('click', saveScenario);
  document.getElementById('btn-share')?.addEventListener('click', copyShareLink);
  document.getElementById('btn-load-scenario').addEventListener('click', () => {
    document.getElementById('scenario-file').click();
  });
  document.getElementById('scenario-file').addEventListener('change', e => {
    if (e.target.files[0]) { loadScenario(e.target.files[0]); e.target.value = ''; }
  });

  // Photo coverage toggle
  document.getElementById('chk-photos').addEventListener('change', e => {
    if (!state.photoGroup) return;
    if (e.target.checked) state.photoGroup.addTo(map);
    else map.removeLayer(state.photoGroup);
  });

  // Swath footprints toggle
  document.getElementById('chk-footprints').addEventListener('change', () => {
    renderSwathFootprints(state.currentMissions || []);
  });

  // Export both plans buttons
  document.getElementById('btn-export-kml-time').addEventListener('click', () => exportPlan('kml', 'min_time'));
  document.getElementById('btn-export-kml-wear').addEventListener('click', () => exportPlan('kml', 'min_wear'));
  document.getElementById('btn-export-gj-time').addEventListener('click', () => exportPlan('geojson', 'min_time'));
  document.getElementById('btn-export-gj-wear').addEventListener('click', () => exportPlan('geojson', 'min_wear'));
}

// ─── Utils ───────────────────────────────────────────────────────────────────
function setStatus(msg, type = '') {
  const el = document.getElementById('status-bar');
  el.className = type;
  el.innerHTML = type === 'loading'
    ? `<span class="spin">⟳</span> ${msg}`
    : msg;
}

async function fetchJSON(url, method = 'GET', body = null, signal = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  if (signal) opts.signal = signal;
  const resp = await fetch(url, opts);
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(err.detail ?? resp.statusText);
  }
  return resp.json();
}

// ─── Demo Tour ───────────────────────────────────────────────────────────────
const TOUR_STEPS = [
  {
    targetId: 'btn-load-demo2',
    title: '1 / 7 — Загрузка сценария',
    body: 'Нажмите «Демо 2 БВС», чтобы загрузить готовый сценарий: 2 зоны съёмки, бесполётная зона и 2 ВПП. Маршруты рассчитаются автоматически.',
    action: () => document.getElementById('btn-load-demo2').click(),
    actionLabel: '▶ Запустить демо',
  },
  {
    targetId: 'area-info',
    title: '2 / 7 — Зона и параметры',
    body: 'Поле «Зона» показывает площадь, количество БЗ, ВПП и расчётный GSD в реальном времени. GSD обновляется при изменении высоты или типа съёмки.',
  },
  {
    targetId: 'btn-plan',
    title: '3 / 7 — Расчёт маршрутов',
    body: 'Кнопка «Рассчитать маршруты» запускает бустрофедонный алгоритм покрытия. Для нескольких зон используется эвристика LPT для оптимального распределения между БПЛА.',
  },
  {
    targetId: 'results-comparison',
    title: '4 / 7 — Сравнение стратегий',
    body: 'Система автоматически сравнивает план «минимум времени» и «минимум износа» и рекомендует лучший вариант с учётом штрафа на запуск каждого БПЛА.',
  },
  {
    targetId: 'results-summary',
    title: '5 / 7 — Результаты и KPI',
    body: 'Карточки миссий содержат: высоту профиля, процент покрытия, рейтинг выполнимости, оценку стоимости, Ганнт-диаграмму и предупреждения по батарее и клиренсу над рельефом.',
  },
  {
    targetId: 'export-row-single',
    title: '6 / 7 — Экспорт',
    body: 'Экспортируйте маршруты в KML (Google Earth), GeoJSON, MAVLink (.waypoints для QGC) или CSV. Доступен HTML-отчёт с полным анализом миссии.',
  },
  {
    targetId: 'btn-weather',
    title: '7 / 7 — Погода и безопасность',
    body: 'Кнопка «Погода» получает прогноз Open-Meteo и определяет лучшее 4-часовое окно вылета. Рельеф оценивается через Digital Elevation Model — система предложит безопасную высоту, если клиренс менее 80 м.',
  },
];

let _tourStep = -1;
let _tourEl = null;
let _tourOverlay = null;

function startTour() {
  endTour();
  _tourStep = 0;
  _tourOverlay = document.createElement('div');
  _tourOverlay.id = 'tour-overlay';
  _tourOverlay.style.cssText = 'position:fixed;inset:0;z-index:19998;pointer-events:none;background:rgba(0,0,0,0.35)';
  document.body.appendChild(_tourOverlay);
  _tourEl = document.createElement('div');
  _tourEl.id = 'tour-card';
  _tourEl.style.cssText = 'position:fixed;z-index:19999;background:var(--surface);border:1px solid var(--accent);border-radius:12px;padding:16px 18px;max-width:320px;box-shadow:0 8px 32px rgba(0,0,0,0.5);font-size:12px;line-height:1.5';
  document.body.appendChild(_tourEl);
  renderTourStep();
}

function renderTourStep() {
  if (!_tourEl) return;
  const step = TOUR_STEPS[_tourStep];
  const target = step.targetId ? document.getElementById(step.targetId) : null;

  // Position card near target
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    const r = target.getBoundingClientRect();
    // Highlight via box-shadow on overlay — punch-out via CSS clip is complex; use outline on element
    target.style.outline = '3px solid var(--accent)';
    target.style.outlineOffset = '3px';
    target.style.borderRadius = '6px';
    target.style.zIndex = '19999';
    target.style.position = target.style.position || 'relative';
    // Position card below or above target
    const cardW = 320, cardH = 200;
    const top = r.bottom + 10 < window.innerHeight - cardH ? r.bottom + 10 : r.top - cardH - 10;
    const left = Math.min(Math.max(r.left, 8), window.innerWidth - cardW - 8);
    _tourEl.style.top = Math.max(8, top) + 'px';
    _tourEl.style.left = left + 'px';
  } else {
    _tourEl.style.top = '50%';
    _tourEl.style.left = '50%';
    _tourEl.style.transform = 'translate(-50%,-50%)';
  }

  const isFirst = _tourStep === 0;
  const isLast = _tourStep === TOUR_STEPS.length - 1;
  _tourEl.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <b style="color:var(--accent);font-size:11px">${step.title}</b>
      <button onclick="endTour()" style="background:none;border:none;cursor:pointer;color:var(--text2);font-size:16px;line-height:1;padding:0">×</button>
    </div>
    <div style="color:var(--text);margin-bottom:12px">${step.body}</div>
    ${step.action ? `<button id="tour-action-btn" class="btn btn-secondary btn-sm" style="width:100%;margin-bottom:8px">${step.actionLabel}</button>` : ''}
    <div style="display:flex;gap:6px;justify-content:space-between;align-items:center">
      <span style="color:var(--text2);font-size:10px">${_tourStep + 1} из ${TOUR_STEPS.length}</span>
      <div style="display:flex;gap:6px">
        ${!isFirst ? `<button onclick="tourNav(-1)" class="btn btn-ghost btn-sm">← Назад</button>` : ''}
        ${!isLast ? `<button onclick="tourNav(1)" class="btn btn-primary btn-sm">Далее →</button>` : `<button onclick="endTour()" class="btn btn-success btn-sm">✅ Завершить</button>`}
      </div>
    </div>
  `;
  document.getElementById('tour-action-btn')?.addEventListener('click', () => {
    step.action();
    setTimeout(() => tourNav(1), 800);
  });
}

function tourNav(dir) {
  // Clear previous highlight
  const prev = TOUR_STEPS[_tourStep];
  if (prev?.targetId) {
    const el = document.getElementById(prev.targetId);
    if (el) { el.style.outline = ''; el.style.outlineOffset = ''; el.style.zIndex = ''; }
  }
  _tourStep = Math.max(0, Math.min(TOUR_STEPS.length - 1, _tourStep + dir));
  renderTourStep();
}

function endTour() {
  // Clear all highlights
  TOUR_STEPS.forEach(s => {
    if (s.targetId) {
      const el = document.getElementById(s.targetId);
      if (el) { el.style.outline = ''; el.style.outlineOffset = ''; el.style.zIndex = ''; }
    }
  });
  document.getElementById('tour-overlay')?.remove();
  document.getElementById('tour-card')?.remove();
  _tourEl = null;
  _tourOverlay = null;
  _tourStep = -1;
}

document.getElementById('btn-tour')?.addEventListener('click', startTour);

// ─── Keyboard shortcuts ───────────────────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'Enter' && !e.ctrlKey) document.getElementById('btn-plan').click();
  if (e.key === 'd' || e.key === 'D') document.getElementById('btn-load-demo').click();
  if (e.key === 'Escape') { endTour(); document.getElementById('btn-clear').click(); }
});

// ─── CSV export ──────────────────────────────────────────────────────────────
document.getElementById('btn-export-footprints')?.addEventListener('click', () => {
  if (!state.currentMissions?.length) return;
  const features = [];
  state.currentMissions.forEach(m => {
    const swath = m.metrics?.swath_m;
    if (!swath) return;
    const startWps = (m.waypoints || []).filter(w => w.action === 'survey_start');
    const endWps = (m.waypoints || []).filter(w => w.action === 'survey_end');
    for (let i = 0; i < Math.min(startWps.length, endWps.length); i++) {
      const a = startWps[i], b = endWps[i];
      const midlat = (a.lat + b.lat) / 2 * Math.PI / 180;
      const dlat_m = (b.lat - a.lat) * 111320;
      const dlon_m = (b.lon - a.lon) * 111320 * Math.cos(midlat);
      const len = Math.sqrt(dlat_m * dlat_m + dlon_m * dlon_m) || 1;
      const pn = -dlon_m / len, pe = dlat_m / len;
      const hw = swath / 2;
      const pLat = pn * hw / 111320;
      const pLon = pe * hw / (111320 * Math.cos(midlat));
      features.push({
        type: 'Feature',
        geometry: { type: 'Polygon', coordinates: [[[a.lon+pLon,a.lat+pLat],[b.lon+pLon,b.lat+pLat],[b.lon-pLon,b.lat-pLat],[a.lon-pLon,a.lat-pLat],[a.lon+pLon,a.lat+pLat]]] },
        properties: { uav: m.uav_name, strip: i + 1, swath_m: swath, gsd_cm: m.metrics?.gsd_cm },
      });
    }
  });
  downloadBlob(new Blob([JSON.stringify({ type:'FeatureCollection', features }, null, 2)], { type:'application/geo+json' }), 'coverage_footprints.geojson');
  setStatus(`Экспортировано ${features.length} полос захвата`, 'ok');
});

document.getElementById('btn-export-csv')?.addEventListener('click', () => {
  if (!state.currentMissions?.length) return;
  const rows = ['UAV,Action,Lat,Lon,Alt_m,Seq'];
  let seq = 0;
  state.currentMissions.forEach(m => {
    (m.waypoints || []).filter(w => w.action !== 'photo').forEach(wp => {
      rows.push([m.uav_name, wp.action, wp.lat.toFixed(8), wp.lon.toFixed(8), (wp.alt_m || 0).toFixed(1), seq++].join(','));
    });
  });
  downloadBlob(new Blob([rows.join('\n')], { type: 'text/csv' }), 'waypoints.csv');
  setStatus('CSV экспортирован', 'ok');
});

// ─── Boot ────────────────────────────────────────────────────────────────────
init().catch(e => setStatus('Ошибка загрузки: ' + e.message, 'error'));
