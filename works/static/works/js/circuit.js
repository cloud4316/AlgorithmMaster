/* ============================================================
   CircuitBuilder — самостоятельный редактор схем для Arduino
   ============================================================ */

'use strict';

// ── Компоненты ───────────────────────────────────────────────────────────────

const CT = {  // Component Types
  arduino_uno: {
    name: 'Arduino Uno', category: 'mcu', icon: '🟦',
    w: 200, h: 260,
    color: '#1a659e',
    props: {},
    pins: [
      // Цифровые пины — правая сторона
      {id:'d13',x:200,y:28,lbl:'~13'}, {id:'d12',x:200,y:48,lbl:'12'},
      {id:'d11',x:200,y:68,lbl:'~11'}, {id:'d10',x:200,y:88,lbl:'~10'},
      {id:'d9', x:200,y:108,lbl:'~9'},  {id:'d8', x:200,y:128,lbl:'8'},
      {id:'d7', x:200,y:148,lbl:'7'},   {id:'d6', x:200,y:168,lbl:'~6'},
      {id:'d5', x:200,y:188,lbl:'~5'},  {id:'d4', x:200,y:208,lbl:'4'},
      {id:'d3', x:200,y:228,lbl:'~3'},  {id:'d2', x:200,y:248,lbl:'2'},
      // Аналоговые пины — левая сторона
      {id:'a0',x:0,y:148,lbl:'A0'}, {id:'a1',x:0,y:168,lbl:'A1'},
      {id:'a2',x:0,y:188,lbl:'A2'}, {id:'a3',x:0,y:208,lbl:'A3'},
      {id:'a4',x:0,y:228,lbl:'A4 SDA'}, {id:'a5',x:0,y:248,lbl:'A5 SCL'},
      // Питание
      {id:'5v', x:0,y:28,lbl:'5V',  type:'vcc'},
      {id:'33v',x:0,y:48,lbl:'3.3V',type:'vcc'},
      {id:'gnd1',x:0,y:68,lbl:'GND',type:'gnd'},
      {id:'gnd2',x:0,y:88,lbl:'GND',type:'gnd'},
      {id:'rst', x:0,y:108,lbl:'RST'},
      {id:'vin', x:0,y:128,lbl:'VIN'},
    ],
    render(c) {
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="6"
              fill="#1a659e" stroke="#0d4a7a" stroke-width="2"/>
        <rect x="4" y="4" width="${c.w-8}" height="${c.h-8}" rx="4"
              fill="none" stroke="#4a9cd0" stroke-width="1" opacity="0.4"/>
        <text x="${c.w/2}" y="14" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">Arduino</text>
        <text x="${c.w/2}" y="26" text-anchor="middle" fill="#93c5fd" font-size="8">UNO</text>
        ${c.type.pins.filter(p=>p.x===200).map(p=>`
          <line x1="${c.w-12}" y1="${p.y}" x2="${c.w}" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="${c.w-12}" y="${p.y-5}" width="10" height="10" rx="2" fill="#1e3a5f"/>
          <text x="${c.w-14}" y="${p.y+3}" text-anchor="end" fill="#93c5fd" font-size="7">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="12" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="2" y="${p.y-5}" width="10" height="10" rx="2" fill="#1e3a5f"/>
          <text x="14" y="${p.y+3}" fill="#93c5fd" font-size="7">${p.lbl}</text>
        `).join('')}`;
    }
  },

  resistor: {
    name: 'Резистор', category: 'passive', icon: '⊓',
    w: 80, h: 30,
    color: '#78350f',
    props: {value: '220 Ω'},
    pins: [{id:'a',x:0,y:15,lbl:''},{id:'b',x:80,y:15,lbl:''}],
    render(c) {
      const v = c.props.value || '?Ω';
      return `<line x1="0" y1="15" x2="20" y2="15" stroke="#d97706" stroke-width="2"/>
        <line x1="60" y1="15" x2="80" y2="15" stroke="#d97706" stroke-width="2"/>
        <rect x="20" y="6" width="40" height="18" rx="3" fill="#92400e" stroke="#d97706" stroke-width="1.5"/>
        <line x1="26" y1="6" x2="26" y2="24" stroke="#fbbf24" stroke-width="3" opacity="0.8"/>
        <line x1="32" y1="6" x2="32" y2="24" stroke="#ef4444" stroke-width="3" opacity="0.8"/>
        <line x1="40" y1="6" x2="40" y2="24" stroke="#fbbf24" stroke-width="3" opacity="0.8"/>
        <line x1="48" y1="6" x2="48" y2="24" stroke="#a3a3a3" stroke-width="3" opacity="0.8"/>
        <text x="40" y="38" text-anchor="middle" fill="#d97706" font-size="9">${v}</text>`;
    }
  },

  led: {
    name: 'Светодиод', category: 'passive', icon: '💡',
    w: 60, h: 30,
    color: '#ef4444',
    props: {color: 'red'},
    pins: [{id:'anode',x:0,y:15,lbl:'+'},{id:'cathode',x:60,y:15,lbl:'-'}],
    colorMap: {red:'#ef4444',green:'#22c55e',yellow:'#eab308',blue:'#3b82f6',white:'#e5e7eb'},
    render(c) {
      const col = this.colorMap[c.props.color||'red'] || '#ef4444';
      const lit  = c._lit;
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="${col}" stroke-width="2"/>
        <line x1="42" y1="15" x2="60" y2="15" stroke="${col}" stroke-width="2"/>
        <polygon points="18,5 18,25 38,15" fill="${lit?col:'none'}" stroke="${col}" stroke-width="1.5"/>
        <line x1="38" y1="5" x2="38" y2="25" stroke="${col}" stroke-width="2"/>
        ${lit?`<circle cx="28" cy="15" r="14" fill="${col}" opacity="0.2"/>
          <line x1="40" y1="4" x2="45" y2="0" stroke="${col}" stroke-width="1.5" opacity="0.7"/>
          <line x1="43" y1="7" x2="49" y2="4" stroke="${col}" stroke-width="1.5" opacity="0.7"/>`:''}
        <text x="30" y="38" text-anchor="middle" fill="${col}" font-size="8">${c.props.color||'red'}</text>`;
    }
  },

  button: {
    name: 'Кнопка', category: 'passive', icon: '⏺',
    w: 60, h: 50,
    color: '#6b7280',
    props: {pressed: false},
    pins: [
      {id:'p1',x:0,y:15,lbl:'1'},{id:'p2',x:60,y:15,lbl:'2'},
      {id:'p3',x:0,y:35,lbl:'3'},{id:'p4',x:60,y:35,lbl:'4'},
    ],
    render(c) {
      const pr = c._pressed;
      return `<line x1="0" y1="15" x2="22" y2="15" stroke="#9ca3af" stroke-width="2"/>
        <line x1="38" y1="15" x2="60" y2="15" stroke="#9ca3af" stroke-width="2"/>
        <line x1="0" y1="35" x2="22" y2="35" stroke="#9ca3af" stroke-width="2"/>
        <line x1="38" y1="35" x2="60" y2="35" stroke="#9ca3af" stroke-width="2"/>
        <line x1="22" y1="10" x2="22" y2="40" stroke="#9ca3af" stroke-width="1.5"/>
        <line x1="38" y1="10" x2="38" y2="40" stroke="#9ca3af" stroke-width="1.5"/>
        ${pr
          ? `<line x1="22" y1="15" x2="38" y2="15" stroke="#60a5fa" stroke-width="2"/>
             <line x1="22" y1="35" x2="38" y2="35" stroke="#60a5fa" stroke-width="2"/>`
          : `<line x1="25" y1="20" x2="35" y2="20" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2"/>
             <line x1="25" y1="30" x2="35" y2="30" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2"/>`}
        <rect x="24" y="18" width="12" height="14" rx="2" fill="${pr?'#3b82f6':'#374151'}" stroke="#6b7280" stroke-width="1"/>
        <text x="30" y="58" text-anchor="middle" fill="#9ca3af" font-size="8">BTN</text>`;
    }
  },

  vcc: {
    name: '+5V / VCC', category: 'power', icon: '⚡',
    w: 30, h: 40,
    color: '#ef4444',
    props: {},
    pins: [{id:'out',x:15,y:40,lbl:''}],
    render() {
      return `<line x1="15" y1="20" x2="15" y2="40" stroke="#ef4444" stroke-width="2"/>
        <line x1="5" y1="20" x2="25" y2="20" stroke="#ef4444" stroke-width="2"/>
        <line x1="8" y1="14" x2="22" y2="14" stroke="#ef4444" stroke-width="2"/>
        <line x1="11" y1="8" x2="19" y2="8" stroke="#ef4444" stroke-width="2"/>
        <text x="15" y="5" text-anchor="middle" fill="#ef4444" font-size="8" font-weight="bold">+5V</text>`;
    }
  },

  gnd: {
    name: 'GND', category: 'power', icon: '⏚',
    w: 30, h: 40,
    color: '#6b7280',
    props: {},
    pins: [{id:'in',x:15,y:0,lbl:''}],
    render() {
      return `<line x1="15" y1="0" x2="15" y2="20" stroke="#6b7280" stroke-width="2"/>
        <line x1="5" y1="20" x2="25" y2="20" stroke="#6b7280" stroke-width="2"/>
        <line x1="8" y1="26" x2="22" y2="26" stroke="#6b7280" stroke-width="2"/>
        <line x1="11" y1="32" x2="19" y2="32" stroke="#6b7280" stroke-width="2"/>
        <text x="15" y="44" text-anchor="middle" fill="#6b7280" font-size="8">GND</text>`;
    }
  },

  buzzer: {
    name: 'Зуммер', category: 'passive', icon: '🔔',
    w: 50, h: 50,
    color: '#8b5cf6',
    props: {},
    pins: [{id:'p',x:0,y:25,lbl:'+'},{id:'n',x:50,y:25,lbl:'-'}],
    render(c) {
      const on = c._lit;
      return `<line x1="0" y1="25" x2="12" y2="25" stroke="#8b5cf6" stroke-width="2"/>
        <line x1="38" y1="25" x2="50" y2="25" stroke="#8b5cf6" stroke-width="2"/>
        <circle cx="25" cy="25" r="14" fill="${on?'#4c1d95':'#1e1b4b'}" stroke="#8b5cf6" stroke-width="2"/>
        ${on?`<text x="25" y="30" text-anchor="middle" fill="#a78bfa" font-size="14">♪</text>`
            :`<text x="25" y="29" text-anchor="middle" fill="#7c3aed" font-size="11">BZZ</text>`}
        <text x="25" y="48" text-anchor="middle" fill="#8b5cf6" font-size="8">Зуммер</text>`;
    }
  },

  wire_node: {
    name: 'Узел', category: 'passive', icon: '●',
    w: 10, h: 10,
    color: '#374151',
    props: {},
    pins: [{id:'c',x:5,y:5,lbl:''}],
    render() {
      return `<circle cx="5" cy="5" r="4" fill="#374151" stroke="#6b7280" stroke-width="1"/>`;
    }
  },

  // ── Microcontrollers ──────────────────────────────────────────────────────
  arduino_nano: {
    name: 'Arduino Nano', category: 'mcu', icon: '🔷',
    w: 100, h: 280,
    color: '#1a659e',
    props: {},
    pins: [
      {id:'d13',x:100,y:30,lbl:'D13'},{id:'d12',x:100,y:50,lbl:'D12'},
      {id:'d11',x:100,y:70,lbl:'D11~'},{id:'d10',x:100,y:90,lbl:'D10~'},
      {id:'d9', x:100,y:110,lbl:'D9~'},{id:'d8', x:100,y:130,lbl:'D8'},
      {id:'d7', x:100,y:150,lbl:'D7'},{id:'d6', x:100,y:170,lbl:'D6~'},
      {id:'d5', x:100,y:190,lbl:'D5~'},{id:'d4', x:100,y:210,lbl:'D4'},
      {id:'d3', x:100,y:230,lbl:'D3~'},{id:'d2', x:100,y:250,lbl:'D2'},
      {id:'a0',x:0,y:110,lbl:'A0'},{id:'a1',x:0,y:130,lbl:'A1'},
      {id:'a2',x:0,y:150,lbl:'A2'},{id:'a3',x:0,y:170,lbl:'A3'},
      {id:'a4',x:0,y:190,lbl:'A4'},{id:'a5',x:0,y:210,lbl:'A5'},
      {id:'a6',x:0,y:230,lbl:'A6'},{id:'a7',x:0,y:250,lbl:'A7'},
      {id:'5v',x:0,y:30,lbl:'5V',type:'vcc'},{id:'33v',x:0,y:50,lbl:'3.3V',type:'vcc'},
      {id:'gnd1',x:0,y:70,lbl:'GND',type:'gnd'},{id:'gnd2',x:0,y:90,lbl:'GND',type:'gnd'},
      {id:'rst',x:0,y:270,lbl:'RST'},{id:'vin',x:100,y:270,lbl:'VIN'},
    ],
    render(c) {
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="4" fill="#1a659e" stroke="#0d4a7a" stroke-width="1.5"/>
        <text x="${c.w/2}" y="14" text-anchor="middle" fill="#fff" font-size="9" font-weight="bold">Arduino</text>
        <text x="${c.w/2}" y="24" text-anchor="middle" fill="#93c5fd" font-size="7">NANO</text>
        ${c.type.pins.filter(p=>p.x===100).map(p=>`
          <line x1="${c.w-8}" y1="${p.y}" x2="${c.w}" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="${c.w-8}" y="${p.y-4}" width="7" height="8" rx="1" fill="#1e3a5f"/>
          <text x="${c.w-10}" y="${p.y+3}" text-anchor="end" fill="#93c5fd" font-size="6">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="8" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="1" y="${p.y-4}" width="7" height="8" rx="1" fill="#1e3a5f"/>
          <text x="10" y="${p.y+3}" fill="#93c5fd" font-size="6">${p.lbl}</text>
        `).join('')}`;
    }
  },

  arduino_mega: {
    name: 'Arduino Mega', category: 'mcu', icon: '🟪',
    w: 240, h: 340,
    color: '#1a3a5e',
    props: {},
    pins: [
      // Right side digital
      {id:'d13',x:240,y:30,lbl:'13'},{id:'d12',x:240,y:48,lbl:'12'},
      {id:'d11',x:240,y:66,lbl:'~11'},{id:'d10',x:240,y:84,lbl:'~10'},
      {id:'d9', x:240,y:102,lbl:'~9'},{id:'d8', x:240,y:120,lbl:'8'},
      {id:'d7', x:240,y:138,lbl:'~7'},{id:'d6', x:240,y:156,lbl:'~6'},
      {id:'d5', x:240,y:174,lbl:'~5'},{id:'d4', x:240,y:192,lbl:'4'},
      {id:'d3', x:240,y:210,lbl:'~3'},{id:'d2', x:240,y:228,lbl:'2'},
      {id:'d1', x:240,y:246,lbl:'TX1'},{id:'d0', x:240,y:264,lbl:'RX0'},
      // Right side extended
      {id:'d22',x:240,y:286,lbl:'22'},{id:'d24',x:240,y:304,lbl:'24'},
      // Left side
      {id:'5v', x:0,y:30,lbl:'5V',type:'vcc'},{id:'33v',x:0,y:50,lbl:'3.3V',type:'vcc'},
      {id:'gnd1',x:0,y:70,lbl:'GND',type:'gnd'},{id:'gnd2',x:0,y:90,lbl:'GND',type:'gnd'},
      {id:'a0',x:0,y:120,lbl:'A0'},{id:'a1',x:0,y:138,lbl:'A1'},
      {id:'a2',x:0,y:156,lbl:'A2'},{id:'a3',x:0,y:174,lbl:'A3'},
      {id:'a4',x:0,y:192,lbl:'A4'},{id:'a5',x:0,y:210,lbl:'A5'},
      {id:'a6',x:0,y:228,lbl:'A6'},{id:'a7',x:0,y:246,lbl:'A7'},
      {id:'a8',x:0,y:264,lbl:'A8'},{id:'a9',x:0,y:282,lbl:'A9'},
      {id:'rst',x:0,y:310,lbl:'RST'},{id:'vin',x:0,y:330,lbl:'VIN'},
    ],
    render(c) {
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="6" fill="#1a3a5e" stroke="#0a2540" stroke-width="2"/>
        <text x="${c.w/2}" y="14" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">Arduino</text>
        <text x="${c.w/2}" y="26" text-anchor="middle" fill="#93c5fd" font-size="8">MEGA 2560</text>
        ${c.type.pins.filter(p=>p.x===240).map(p=>`
          <line x1="${c.w-12}" y1="${p.y}" x2="${c.w}" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="${c.w-12}" y="${p.y-5}" width="10" height="10" rx="1" fill="#1e3a5f"/>
          <text x="${c.w-14}" y="${p.y+3}" text-anchor="end" fill="#93c5fd" font-size="6">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="12" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="2" y="${p.y-5}" width="10" height="10" rx="1" fill="#1e3a5f"/>
          <text x="14" y="${p.y+3}" fill="#93c5fd" font-size="6">${p.lbl}</text>
        `).join('')}`;
    }
  },

  esp8266: {
    name: 'ESP8266 (NodeMCU)', category: 'mcu', icon: '📶',
    w: 100, h: 240,
    color: '#065f46',
    props: {},
    pins: [
      {id:'d0',x:100,y:30,lbl:'D0'},{id:'d1',x:100,y:50,lbl:'D1'},
      {id:'d2',x:100,y:70,lbl:'D2'},{id:'d3',x:100,y:90,lbl:'D3'},
      {id:'d4',x:100,y:110,lbl:'D4'},{id:'d5',x:100,y:130,lbl:'D5'},
      {id:'d6',x:100,y:150,lbl:'D6'},{id:'d7',x:100,y:170,lbl:'D7'},
      {id:'d8',x:100,y:190,lbl:'D8'},
      {id:'3v3',x:0,y:30,lbl:'3.3V',type:'vcc'},{id:'gnd',x:0,y:50,lbl:'GND',type:'gnd'},
      {id:'vin',x:0,y:70,lbl:'VIN'},{id:'a0',x:0,y:90,lbl:'A0'},
      {id:'rx',x:0,y:130,lbl:'RX'},{id:'tx',x:0,y:150,lbl:'TX'},
      {id:'rst',x:0,y:220,lbl:'RST'},
    ],
    render(c) {
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="5" fill="#065f46" stroke="#022c22" stroke-width="1.5"/>
        <rect x="20" y="4" width="60" height="16" rx="3" fill="#10b981" opacity="0.3"/>
        <text x="${c.w/2}" y="13" text-anchor="middle" fill="#6ee7b7" font-size="7" font-weight="bold">ESP8266</text>
        <text x="${c.w/2}" y="23" text-anchor="middle" fill="#34d399" font-size="6">NodeMCU</text>
        ${c.type.pins.filter(p=>p.x===100).map(p=>`
          <line x1="${c.w-8}" y1="${p.y}" x2="${c.w}" y2="${p.y}" stroke="#34d399" stroke-width="1.5"/>
          <text x="${c.w-10}" y="${p.y+3}" text-anchor="end" fill="#34d399" font-size="6">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="8" y2="${p.y}" stroke="#34d399" stroke-width="1.5"/>
          <text x="10" y="${p.y+3}" fill="#34d399" font-size="6">${p.lbl}</text>
        `).join('')}`;
    }
  },

  // ── Power ─────────────────────────────────────────────────────────────────
  vcc_3v3: {
    name: '+3.3V', category: 'power', icon: '⚡',
    w: 36, h: 40,
    color: '#f97316',
    props: {},
    pins: [{id:'out',x:18,y:40,lbl:'',type:'vcc'}],
    render() {
      return `<line x1="18" y1="20" x2="18" y2="40" stroke="#f97316" stroke-width="2"/>
        <line x1="6" y1="20" x2="30" y2="20" stroke="#f97316" stroke-width="2"/>
        <line x1="9" y1="14" x2="27" y2="14" stroke="#f97316" stroke-width="2"/>
        <line x1="12" y1="8" x2="24" y2="8" stroke="#f97316" stroke-width="2"/>
        <text x="18" y="5" text-anchor="middle" fill="#f97316" font-size="7" font-weight="bold">3.3V</text>`;
    }
  },

  battery_9v: {
    name: 'Батарея 9V', category: 'power', icon: '🔋',
    w: 60, h: 80,
    color: '#374151',
    props: {},
    pins: [
      {id:'pos',x:15,y:0,lbl:'+',type:'vcc'},
      {id:'neg',x:45,y:0,lbl:'-',type:'gnd'},
    ],
    render() {
      return `<rect x="5" y="10" width="50" height="65" rx="5" fill="#374151" stroke="#6b7280" stroke-width="1.5"/>
        <rect x="15" y="4" width="12" height="8" rx="2" fill="#ef4444"/>
        <rect x="33" y="4" width="12" height="8" rx="2" fill="#6b7280"/>
        <line x1="15" y1="0" x2="15" y2="10" stroke="#ef4444" stroke-width="2"/>
        <line x1="45" y1="0" x2="45" y2="10" stroke="#6b7280" stroke-width="2"/>
        <text x="30" y="45" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">9V</text>
        <text x="17" y="30" text-anchor="middle" fill="#ef4444" font-size="10" font-weight="bold">+</text>
        <text x="43" y="30" text-anchor="middle" fill="#9ca3af" font-size="10" font-weight="bold">−</text>`;
    }
  },

  // ── Passive ───────────────────────────────────────────────────────────────
  capacitor: {
    name: 'Конденсатор', category: 'passive', icon: '⊣⊢',
    w: 50, h: 30,
    color: '#0369a1',
    props: {value: '100 µF'},
    pins: [{id:'p',x:0,y:15,lbl:'+'},{id:'n',x:50,y:15,lbl:'-'}],
    render(c) {
      const v = c.props.value || '?';
      return `<line x1="0" y1="15" x2="20" y2="15" stroke="#0369a1" stroke-width="2"/>
        <line x1="30" y1="15" x2="50" y2="15" stroke="#0369a1" stroke-width="2"/>
        <line x1="20" y1="4" x2="20" y2="26" stroke="#0369a1" stroke-width="3"/>
        <line x1="30" y1="4" x2="30" y2="26" stroke="#0369a1" stroke-width="3"/>
        <text x="25" y="38" text-anchor="middle" fill="#0369a1" font-size="8">${v}</text>
        <text x="18" y="38" text-anchor="middle" fill="#ef4444" font-size="9">+</text>`;
    }
  },

  capacitor_c: {
    name: 'Конд. керамич.', category: 'passive', icon: '⌣',
    w: 50, h: 30,
    color: '#7c3aed',
    props: {value: '0.1 µF'},
    pins: [{id:'a',x:0,y:15,lbl:''},{id:'b',x:50,y:15,lbl:''}],
    render(c) {
      const v = c.props.value || '?';
      return `<line x1="0" y1="15" x2="20" y2="15" stroke="#7c3aed" stroke-width="2"/>
        <line x1="30" y1="15" x2="50" y2="15" stroke="#7c3aed" stroke-width="2"/>
        <path d="M20,5 Q25,15 20,25" fill="none" stroke="#7c3aed" stroke-width="2.5"/>
        <path d="M30,5 Q25,15 30,25" fill="none" stroke="#7c3aed" stroke-width="2.5"/>
        <text x="25" y="38" text-anchor="middle" fill="#7c3aed" font-size="8">${v}</text>`;
    }
  },

  diode: {
    name: 'Диод', category: 'passive', icon: '▷|',
    w: 60, h: 30,
    color: '#92400e',
    props: {type: '1N4007'},
    pins: [{id:'a',x:0,y:15,lbl:'A'},{id:'k',x:60,y:15,lbl:'K'}],
    render(c) {
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="#92400e" stroke-width="2"/>
        <line x1="42" y1="15" x2="60" y2="15" stroke="#92400e" stroke-width="2"/>
        <polygon points="18,5 18,25 38,15" fill="#92400e" stroke="#d97706" stroke-width="1.5"/>
        <line x1="38" y1="5" x2="38" y2="25" stroke="#d97706" stroke-width="2.5"/>
        <text x="30" y="38" text-anchor="middle" fill="#92400e" font-size="7">${c.props.type||'диод'}</text>`;
    }
  },

  zener: {
    name: 'Стабилитрон', category: 'passive', icon: '▷Z',
    w: 60, h: 30,
    color: '#7e22ce',
    props: {voltage: '5.1V'},
    pins: [{id:'a',x:0,y:15,lbl:'A'},{id:'k',x:60,y:15,lbl:'K'}],
    render(c) {
      const v = c.props.voltage || '?V';
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="#7e22ce" stroke-width="2"/>
        <line x1="42" y1="15" x2="60" y2="15" stroke="#7e22ce" stroke-width="2"/>
        <polygon points="18,5 18,25 38,15" fill="#7e22ce" stroke="#a855f7" stroke-width="1.5"/>
        <line x1="35" y1="5" x2="41" y2="5" stroke="#a855f7" stroke-width="2"/>
        <line x1="38" y1="5" x2="38" y2="25" stroke="#a855f7" stroke-width="2.5"/>
        <line x1="38" y1="25" x2="44" y2="25" stroke="#a855f7" stroke-width="2"/>
        <text x="30" y="38" text-anchor="middle" fill="#7e22ce" font-size="8">${v}</text>`;
    }
  },

  potentiometer: {
    name: 'Потенциометр', category: 'passive', icon: '⌁',
    w: 80, h: 55,
    color: '#78350f',
    props: {value: '10 kΩ'},
    pins: [
      {id:'a',x:0,y:20,lbl:'A'},
      {id:'b',x:80,y:20,lbl:'B'},
      {id:'w',x:40,y:55,lbl:'W'},
    ],
    render(c) {
      const v = c.props.value || '?Ω';
      return `<line x1="0" y1="20" x2="20" y2="20" stroke="#d97706" stroke-width="2"/>
        <line x1="60" y1="20" x2="80" y2="20" stroke="#d97706" stroke-width="2"/>
        <rect x="20" y="11" width="40" height="18" rx="3" fill="#92400e" stroke="#d97706" stroke-width="1.5"/>
        <line x1="40" y1="20" x2="40" y2="40" stroke="#d97706" stroke-width="1.5" stroke-dasharray="3,2"/>
        <line x1="34" y1="35" x2="46" y2="45" stroke="#d97706" stroke-width="2"/>
        <line x1="40" y1="45" x2="40" y2="55" stroke="#d97706" stroke-width="2"/>
        <text x="40" y="8" text-anchor="middle" fill="#d97706" font-size="8">${v}</text>`;
    }
  },

  ldr: {
    name: 'Фоторезистор (LDR)', category: 'passive', icon: '☀',
    w: 60, h: 40,
    color: '#16a34a',
    props: {},
    pins: [{id:'a',x:0,y:20,lbl:''},{id:'b',x:60,y:20,lbl:''}],
    render() {
      return `<line x1="0" y1="20" x2="15" y2="20" stroke="#16a34a" stroke-width="2"/>
        <line x1="45" y1="20" x2="60" y2="20" stroke="#16a34a" stroke-width="2"/>
        <rect x="15" y="11" width="30" height="18" rx="3" fill="#14532d" stroke="#16a34a" stroke-width="1.5"/>
        <path d="M20,8 Q25,4 30,8 Q35,4 40,8" fill="none" stroke="#fbbf24" stroke-width="1.5"/>
        <line x1="25" y1="3" x2="22" y2="7" stroke="#fbbf24" stroke-width="1.2"/>
        <line x1="35" y1="3" x2="38" y2="7" stroke="#fbbf24" stroke-width="1.2"/>
        <text x="30" y="38" text-anchor="middle" fill="#16a34a" font-size="7">LDR</text>`;
    }
  },

  thermistor: {
    name: 'Термистор (NTC)', category: 'passive', icon: '🌡',
    w: 60, h: 30,
    color: '#dc2626',
    props: {value: '10 kΩ'},
    pins: [{id:'a',x:0,y:15,lbl:''},{id:'b',x:60,y:15,lbl:''}],
    render(c) {
      return `<line x1="0" y1="15" x2="15" y2="15" stroke="#dc2626" stroke-width="2"/>
        <line x1="45" y1="15" x2="60" y2="15" stroke="#dc2626" stroke-width="2"/>
        <rect x="15" y="6" width="30" height="18" rx="3" fill="#7f1d1d" stroke="#dc2626" stroke-width="1.5"/>
        <line x1="15" y1="22" x2="45" y2="8" stroke="#fca5a5" stroke-width="1.5"/>
        <text x="30" y="38" text-anchor="middle" fill="#dc2626" font-size="7">NTC</text>`;
    }
  },

  // ── Transistors ───────────────────────────────────────────────────────────
  npn: {
    name: 'Транзистор NPN', category: 'transistor', icon: 'NPN',
    w: 60, h: 80,
    color: '#0f766e',
    props: {type: 'BC547'},
    pins: [
      {id:'b',x:0,y:40,lbl:'B'},
      {id:'c',x:60,y:10,lbl:'C'},
      {id:'e',x:60,y:70,lbl:'E'},
    ],
    render(c) {
      return `<line x1="0" y1="40" x2="25" y2="40" stroke="#0f766e" stroke-width="2"/>
        <line x1="25" y1="20" x2="25" y2="60" stroke="#0f766e" stroke-width="3"/>
        <line x1="25" y1="25" x2="60" y2="10" stroke="#0f766e" stroke-width="2"/>
        <line x1="25" y1="55" x2="60" y2="70" stroke="#0f766e" stroke-width="2"/>
        <polygon points="42,60 50,63 48,55" fill="#0f766e"/>
        <text x="30" y="47" fill="#0f766e" font-size="7">NPN</text>
        <text x="30" y="80" text-anchor="middle" fill="#0f766e" font-size="7">${c.props.type||''}</text>`;
    }
  },

  pnp: {
    name: 'Транзистор PNP', category: 'transistor', icon: 'PNP',
    w: 60, h: 80,
    color: '#7c3aed',
    props: {type: 'BC557'},
    pins: [
      {id:'b',x:0,y:40,lbl:'B'},
      {id:'c',x:60,y:10,lbl:'C'},
      {id:'e',x:60,y:70,lbl:'E'},
    ],
    render(c) {
      return `<line x1="0" y1="40" x2="25" y2="40" stroke="#7c3aed" stroke-width="2"/>
        <line x1="25" y1="20" x2="25" y2="60" stroke="#7c3aed" stroke-width="3"/>
        <line x1="25" y1="25" x2="60" y2="10" stroke="#7c3aed" stroke-width="2"/>
        <line x1="25" y1="55" x2="60" y2="70" stroke="#7c3aed" stroke-width="2"/>
        <polygon points="28,27 36,24 34,32" fill="#7c3aed"/>
        <text x="30" y="47" fill="#7c3aed" font-size="7">PNP</text>
        <text x="30" y="80" text-anchor="middle" fill="#7c3aed" font-size="7">${c.props.type||''}</text>`;
    }
  },

  mosfet_n: {
    name: 'MOSFET N-ch', category: 'transistor', icon: 'FET',
    w: 60, h: 80,
    color: '#0369a1',
    props: {type: 'IRF540'},
    pins: [
      {id:'g',x:0,y:40,lbl:'G'},
      {id:'d',x:60,y:10,lbl:'D'},
      {id:'s',x:60,y:70,lbl:'S'},
    ],
    render(c) {
      return `<line x1="0" y1="40" x2="20" y2="40" stroke="#0369a1" stroke-width="2"/>
        <line x1="20" y1="25" x2="20" y2="55" stroke="#0369a1" stroke-width="2"/>
        <line x1="22" y1="25" x2="22" y2="55" stroke="#0369a1" stroke-width="3"/>
        <line x1="22" y1="25" x2="40" y2="25" stroke="#0369a1" stroke-width="2"/>
        <line x1="22" y1="55" x2="40" y2="55" stroke="#0369a1" stroke-width="2"/>
        <line x1="40" y1="25" x2="40" y2="10" stroke="#0369a1" stroke-width="2"/>
        <line x1="40" y1="55" x2="40" y2="70" stroke="#0369a1" stroke-width="2"/>
        <line x1="40" y1="10" x2="60" y2="10" stroke="#0369a1" stroke-width="2"/>
        <line x1="40" y1="70" x2="60" y2="70" stroke="#0369a1" stroke-width="2"/>
        <polygon points="30,50 38,55 38,45" fill="#0369a1"/>
        <text x="30" y="80" text-anchor="middle" fill="#0369a1" font-size="7">${c.props.type||'MOSFET'}</text>`;
    }
  },

  // ── Logic Gates ───────────────────────────────────────────────────────────
  gate_not: {
    name: 'НЕ (NOT)', category: 'gate', icon: '¬',
    w: 60, h: 40,
    color: '#0891b2',
    props: {},
    pins: [{id:'a',x:0,y:20,lbl:'A'},{id:'q',x:60,y:20,lbl:'Q'}],
    render() {
      return `<line x1="0" y1="20" x2="14" y2="20" stroke="#0891b2" stroke-width="2"/>
        <line x1="54" y1="20" x2="60" y2="20" stroke="#0891b2" stroke-width="2"/>
        <path d="M14,5 L14,35 L46,20 Z" fill="#e0f2fe" stroke="#0891b2" stroke-width="1.5"/>
        <circle cx="50" cy="20" r="4" fill="#e0f2fe" stroke="#0891b2" stroke-width="1.5"/>
        <text x="30" y="50" text-anchor="middle" fill="#0891b2" font-size="8">NOT</text>`;
    }
  },

  gate_and: {
    name: 'И (AND)', category: 'gate', icon: '&',
    w: 70, h: 60,
    color: '#059669',
    props: {},
    pins: [
      {id:'a',x:0,y:15,lbl:'A'},{id:'b',x:0,y:45,lbl:'B'},
      {id:'q',x:70,y:30,lbl:'Q'}
    ],
    render() {
      return `<line x1="0" y1="15" x2="20" y2="15" stroke="#059669" stroke-width="2"/>
        <line x1="0" y1="45" x2="20" y2="45" stroke="#059669" stroke-width="2"/>
        <line x1="60" y1="30" x2="70" y2="30" stroke="#059669" stroke-width="2"/>
        <path d="M20,5 L20,55 L40,55 Q62,55 62,30 Q62,5 40,5 Z" fill="#d1fae5" stroke="#059669" stroke-width="1.5"/>
        <text x="35" y="65" text-anchor="middle" fill="#059669" font-size="8">AND</text>`;
    }
  },

  gate_or: {
    name: 'ИЛИ (OR)', category: 'gate', icon: '≥1',
    w: 70, h: 60,
    color: '#d97706',
    props: {},
    pins: [
      {id:'a',x:0,y:15,lbl:'A'},{id:'b',x:0,y:45,lbl:'B'},
      {id:'q',x:70,y:30,lbl:'Q'}
    ],
    render() {
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="#d97706" stroke-width="2"/>
        <line x1="0" y1="45" x2="18" y2="45" stroke="#d97706" stroke-width="2"/>
        <line x1="62" y1="30" x2="70" y2="30" stroke="#d97706" stroke-width="2"/>
        <path d="M15,5 Q28,30 15,55 L40,55 Q66,55 64,30 Q62,5 40,5 Q28,5 15,5 Z"
              fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="38" y="65" text-anchor="middle" fill="#d97706" font-size="8">OR</text>`;
    }
  },

  gate_xor: {
    name: 'ИСКЛ.ИЛИ (XOR)', category: 'gate', icon: '=1',
    w: 70, h: 60,
    color: '#7c3aed',
    props: {},
    pins: [
      {id:'a',x:0,y:15,lbl:'A'},{id:'b',x:0,y:45,lbl:'B'},
      {id:'q',x:70,y:30,lbl:'Q'}
    ],
    render() {
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="#7c3aed" stroke-width="2"/>
        <line x1="0" y1="45" x2="18" y2="45" stroke="#7c3aed" stroke-width="2"/>
        <line x1="62" y1="30" x2="70" y2="30" stroke="#7c3aed" stroke-width="2"/>
        <path d="M18,5 Q31,30 18,55 L42,55 Q68,55 66,30 Q64,5 42,5 Q31,5 18,5 Z"
              fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
        <path d="M10,5 Q23,30 10,55" fill="none" stroke="#7c3aed" stroke-width="1.5"/>
        <text x="38" y="65" text-anchor="middle" fill="#7c3aed" font-size="8">XOR</text>`;
    }
  },

  gate_nand: {
    name: 'НЕ-И (NAND)', category: 'gate', icon: '↑',
    w: 76, h: 60,
    color: '#dc2626',
    props: {},
    pins: [
      {id:'a',x:0,y:15,lbl:'A'},{id:'b',x:0,y:45,lbl:'B'},
      {id:'q',x:76,y:30,lbl:'Q'}
    ],
    render() {
      return `<line x1="0" y1="15" x2="20" y2="15" stroke="#dc2626" stroke-width="2"/>
        <line x1="0" y1="45" x2="20" y2="45" stroke="#dc2626" stroke-width="2"/>
        <line x1="68" y1="30" x2="76" y2="30" stroke="#dc2626" stroke-width="2"/>
        <path d="M20,5 L20,55 L40,55 Q62,55 62,30 Q62,5 40,5 Z" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
        <circle cx="66" cy="30" r="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
        <text x="38" y="65" text-anchor="middle" fill="#dc2626" font-size="8">NAND</text>`;
    }
  },

  gate_nor: {
    name: 'НЕ-ИЛИ (NOR)', category: 'gate', icon: '↓',
    w: 76, h: 60,
    color: '#0f766e',
    props: {},
    pins: [
      {id:'a',x:0,y:15,lbl:'A'},{id:'b',x:0,y:45,lbl:'B'},
      {id:'q',x:76,y:30,lbl:'Q'}
    ],
    render() {
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="#0f766e" stroke-width="2"/>
        <line x1="0" y1="45" x2="18" y2="45" stroke="#0f766e" stroke-width="2"/>
        <line x1="68" y1="30" x2="76" y2="30" stroke="#0f766e" stroke-width="2"/>
        <path d="M15,5 Q28,30 15,55 L40,55 Q66,55 64,30 Q62,5 40,5 Q28,5 15,5 Z"
              fill="#ccfbf1" stroke="#0f766e" stroke-width="1.5"/>
        <circle cx="66" cy="30" r="4" fill="#ccfbf1" stroke="#0f766e" stroke-width="1.5"/>
        <text x="38" y="65" text-anchor="middle" fill="#0f766e" font-size="8">NOR</text>`;
    }
  },

  // ── Display ───────────────────────────────────────────────────────────────
  led_7seg: {
    name: '7-сегм. дисплей', category: 'display', icon: '7',
    w: 70, h: 110,
    color: '#b45309',
    props: {digit: '8', common: 'cathode'},
    pins: [
      {id:'a', x:0,y:20,lbl:'a'},{id:'b', x:0,y:35,lbl:'b'},
      {id:'c', x:0,y:50,lbl:'c'},{id:'d', x:0,y:65,lbl:'d'},
      {id:'e', x:0,y:80,lbl:'e'},{id:'f', x:0,y:95,lbl:'f'},
      {id:'g', x:0,y:110,lbl:'g'},{id:'dp',x:70,y:110,lbl:'dp'},
      {id:'com',x:70,y:20,lbl:'COM'},
    ],
    render(c) {
      // Simple 7-segment digit visual
      const d = c.props.digit || '8';
      return `<rect x="10" y="0" width="60" height="110" rx="4" fill="#1c1917" stroke="#b45309" stroke-width="1.5"/>
        <!-- Top -->
        <line x1="20" y1="8" x2="60" y2="8" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <!-- Top-Left / Top-Right -->
        <line x1="17" y1="10" x2="17" y2="48" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <line x1="63" y1="10" x2="63" y2="48" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <!-- Middle -->
        <line x1="20" y1="52" x2="60" y2="52" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <!-- Bot-Left / Bot-Right -->
        <line x1="17" y1="54" x2="17" y2="92" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <line x1="63" y1="54" x2="63" y2="92" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <!-- Bottom -->
        <line x1="20" y1="94" x2="60" y2="94" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
        <!-- DP -->
        <circle cx="67" cy="94" r="3" fill="#ef4444"/>
        <text x="40" y="108" text-anchor="middle" fill="#b45309" font-size="7">7-SEG</text>`;
    }
  },

  lcd_16x2: {
    name: 'LCD 16x2', category: 'display', icon: '▬',
    w: 200, h: 80,
    color: '#166534',
    props: {backlight: 'on'},
    pins: [
      {id:'vss',x:0,y:20,lbl:'VSS',type:'gnd'},{id:'vdd',x:0,y:35,lbl:'VDD',type:'vcc'},
      {id:'v0', x:0,y:50,lbl:'V0'}, {id:'rs', x:0,y:65,lbl:'RS'},
      {id:'rw', x:200,y:20,lbl:'RW'},{id:'e',  x:200,y:35,lbl:'E'},
      {id:'d4', x:200,y:50,lbl:'D4'},{id:'d5', x:200,y:65,lbl:'D5'},
      {id:'d6', x:0,  y:80,lbl:'D6'},{id:'d7', x:200,y:80,lbl:'D7'},
      {id:'a',  x:0,  y:10,lbl:'A',type:'vcc'},{id:'k',x:200,y:10,lbl:'K',type:'gnd'},
    ],
    render(c) {
      const lit = c.props.backlight !== 'off';
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="5"
                fill="${lit?'#14532d':'#1c1917'}" stroke="#166534" stroke-width="2"/>
        <rect x="8" y="12" width="184" height="58" rx="3" fill="${lit?'#4ade80':'#374151'}" opacity="${lit?0.2:0.1}"/>
        <text x="${c.w/2}" y="35" text-anchor="middle" fill="${lit?'#86efac':'#6b7280'}" font-size="8">LCD 16x2</text>
        <text x="${c.w/2}" y="50" text-anchor="middle" fill="${lit?'#86efac':'#6b7280'}" font-size="7">Hello World!</text>
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="8" y2="${p.y}" stroke="#166534" stroke-width="1.5"/>
          <text x="10" y="${p.y+3}" fill="#4ade80" font-size="6">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===200).map(p=>`
          <line x1="${c.w-8}" y1="${p.y}" x2="${c.w}" y2="${p.y}" stroke="#166534" stroke-width="1.5"/>
          <text x="${c.w-10}" y="${p.y+3}" text-anchor="end" fill="#4ade80" font-size="6">${p.lbl}</text>
        `).join('')}`;
    }
  },

  oled_128x64: {
    name: 'OLED 128x64 (I2C)', category: 'display', icon: '⬛',
    w: 100, h: 50,
    color: '#1e293b',
    props: {address: '0x3C'},
    pins: [
      {id:'vcc',x:0,y:15,lbl:'VCC',type:'vcc'},
      {id:'gnd',x:0,y:30,lbl:'GND',type:'gnd'},
      {id:'scl',x:100,y:15,lbl:'SCL'},
      {id:'sda',x:100,y:30,lbl:'SDA'},
    ],
    render(c) {
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="4" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
        <rect x="6" y="6" width="88" height="38" rx="2" fill="#1e293b"/>
        <text x="${c.w/2}" y="22" text-anchor="middle" fill="#60a5fa" font-size="7" font-weight="bold">OLED</text>
        <text x="${c.w/2}" y="33" text-anchor="middle" fill="#475569" font-size="6">128x64 I2C</text>
        <text x="${c.w/2}" y="43" text-anchor="middle" fill="#334155" font-size="5">${c.props.address}</text>`;
    }
  },

  // ── Sensors ───────────────────────────────────────────────────────────────
  dht11: {
    name: 'DHT11 (темп/влаж)', category: 'sensor', icon: '🌡',
    w: 50, h: 70,
    color: '#0284c7',
    props: {},
    pins: [
      {id:'vcc', x:0,y:20,lbl:'VCC',type:'vcc'},
      {id:'data',x:0,y:40,lbl:'DATA'},
      {id:'gnd', x:0,y:60,lbl:'GND',type:'gnd'},
    ],
    render() {
      return `<rect x="5" y="0" width="45" height="70" rx="5" fill="#0c4a6e" stroke="#0284c7" stroke-width="1.5"/>
        <rect x="10" y="5" width="35" height="35" rx="3" fill="#075985" stroke="#0369a1" stroke-width="1"/>
        <text x="27" y="20" text-anchor="middle" fill="#7dd3fc" font-size="9" font-weight="bold">DHT</text>
        <text x="27" y="32" text-anchor="middle" fill="#38bdf8" font-size="9">11</text>
        <line x1="0" y1="20" x2="5" y2="20" stroke="#0284c7" stroke-width="2"/>
        <line x1="0" y1="40" x2="5" y2="40" stroke="#0284c7" stroke-width="2"/>
        <line x1="0" y1="60" x2="5" y2="60" stroke="#0284c7" stroke-width="2"/>
        <text x="7" y="55" fill="#38bdf8" font-size="6">VCC</text>
        <text x="7" y="45" fill="#38bdf8" font-size="6">DAT</text>
        <text x="7" y="65" fill="#38bdf8" font-size="6">GND</text>`;
    }
  },

  dht22: {
    name: 'DHT22 / AM2302', category: 'sensor', icon: '🌡',
    w: 55, h: 80,
    color: '#0284c7',
    props: {},
    pins: [
      {id:'vcc', x:0,y:20,lbl:'VCC',type:'vcc'},
      {id:'data',x:0,y:40,lbl:'DATA'},
      {id:'nc',  x:0,y:60,lbl:'NC'},
      {id:'gnd', x:0,y:75,lbl:'GND',type:'gnd'},
    ],
    render() {
      return `<rect x="5" y="0" width="50" height="80" rx="5" fill="#0c4a6e" stroke="#0284c7" stroke-width="1.5"/>
        <rect x="10" y="5" width="38" height="35" rx="3" fill="#075985" stroke="#0369a1" stroke-width="1"/>
        <text x="29" y="22" text-anchor="middle" fill="#7dd3fc" font-size="9" font-weight="bold">DHT</text>
        <text x="29" y="34" text-anchor="middle" fill="#38bdf8" font-size="9">22</text>
        <line x1="0" y1="20" x2="5" y2="20" stroke="#0284c7" stroke-width="2"/>
        <line x1="0" y1="40" x2="5" y2="40" stroke="#0284c7" stroke-width="2"/>
        <line x1="0" y1="60" x2="5" y2="60" stroke="#0284c7" stroke-width="2"/>
        <line x1="0" y1="75" x2="5" y2="75" stroke="#0284c7" stroke-width="2"/>`;
    }
  },

  hc_sr04: {
    name: 'HC-SR04 (ультразвук)', category: 'sensor', icon: '📡',
    w: 90, h: 70,
    color: '#0891b2',
    props: {},
    pins: [
      {id:'vcc', x:0,y:20,lbl:'VCC',type:'vcc'},
      {id:'trig',x:0,y:35,lbl:'TRIG'},
      {id:'echo',x:0,y:50,lbl:'ECHO'},
      {id:'gnd', x:0,y:65,lbl:'GND',type:'gnd'},
    ],
    render() {
      return `<rect x="0" y="0" width="90" height="70" rx="4" fill="#0c4a6e" stroke="#0891b2" stroke-width="1.5"/>
        <circle cx="28" cy="28" r="18" fill="#164e63" stroke="#0891b2" stroke-width="1.5"/>
        <circle cx="28" cy="28" r="10" fill="#0e7490"/>
        <circle cx="28" cy="28" r="4" fill="#22d3ee"/>
        <circle cx="62" cy="28" r="18" fill="#164e63" stroke="#0891b2" stroke-width="1.5"/>
        <circle cx="62" cy="28" r="10" fill="#0e7490"/>
        <circle cx="62" cy="28" r="4" fill="#22d3ee"/>
        <text x="45" y="58" text-anchor="middle" fill="#67e8f9" font-size="7">HC-SR04</text>
        <line x1="0" y1="20" x2="8" y2="20" stroke="#22d3ee" stroke-width="1.5"/>
        <line x1="0" y1="35" x2="8" y2="35" stroke="#22d3ee" stroke-width="1.5"/>
        <line x1="0" y1="50" x2="8" y2="50" stroke="#22d3ee" stroke-width="1.5"/>
        <line x1="0" y1="65" x2="8" y2="65" stroke="#22d3ee" stroke-width="1.5"/>`;
    }
  },

  ir_sensor: {
    name: 'ИК датчик препятствий', category: 'sensor', icon: '👁',
    w: 70, h: 55,
    color: '#b45309',
    props: {},
    pins: [
      {id:'vcc',x:0,y:15,lbl:'VCC',type:'vcc'},
      {id:'gnd',x:0,y:30,lbl:'GND',type:'gnd'},
      {id:'out',x:0,y:45,lbl:'OUT'},
    ],
    render() {
      return `<rect x="0" y="0" width="70" height="55" rx="4" fill="#1c1917" stroke="#b45309" stroke-width="1.5"/>
        <circle cx="28" cy="25" r="12" fill="#292524" stroke="#d97706" stroke-width="1"/>
        <circle cx="28" cy="25" r="6" fill="#7c2d12"/>
        <circle cx="50" cy="25" r="12" fill="#292524" stroke="#78716c" stroke-width="1"/>
        <circle cx="50" cy="25" r="6" fill="#3f3f46"/>
        <text x="35" y="48" text-anchor="middle" fill="#d97706" font-size="6">IR Sensor</text>
        <line x1="0" y1="15" x2="8" y2="15" stroke="#d97706" stroke-width="1.5"/>
        <line x1="0" y1="30" x2="8" y2="30" stroke="#d97706" stroke-width="1.5"/>
        <line x1="0" y1="45" x2="8" y2="45" stroke="#d97706" stroke-width="1.5"/>`;
    }
  },

  pir: {
    name: 'PIR датчик движения', category: 'sensor', icon: '👤',
    w: 60, h: 70,
    color: '#b45309',
    props: {},
    pins: [
      {id:'vcc',x:0,y:20,lbl:'VCC',type:'vcc'},
      {id:'out',x:0,y:40,lbl:'OUT'},
      {id:'gnd',x:0,y:60,lbl:'GND',type:'gnd'},
    ],
    render() {
      return `<rect x="5" y="0" width="55" height="70" rx="5" fill="#1c1917" stroke="#b45309" stroke-width="1.5"/>
        <circle cx="32" cy="28" r="20" fill="#292524" stroke="#d97706" stroke-width="1.5"/>
        <circle cx="32" cy="28" r="15" fill="#3f3f46" opacity="0.6"/>
        <circle cx="32" cy="28" r="8" fill="#78350f"/>
        <text x="32" y="58" text-anchor="middle" fill="#d97706" font-size="6">PIR Motion</text>
        <line x1="0" y1="20" x2="5" y2="20" stroke="#d97706" stroke-width="1.5"/>
        <line x1="0" y1="40" x2="5" y2="40" stroke="#d97706" stroke-width="1.5"/>
        <line x1="0" y1="60" x2="5" y2="60" stroke="#d97706" stroke-width="1.5"/>`;
    }
  },

  // ── Actuators ─────────────────────────────────────────────────────────────
  servo: {
    name: 'Сервопривод', category: 'actuator', icon: '⚙',
    w: 80, h: 70,
    color: '#0369a1',
    props: {angle: '90'},
    pins: [
      {id:'gnd',  x:0,y:25,lbl:'GND',type:'gnd'},
      {id:'vcc',  x:0,y:40,lbl:'VCC',type:'vcc'},
      {id:'sig',  x:0,y:55,lbl:'SIG'},
    ],
    render(c) {
      const ang = parseFloat(c.props.angle || 90);
      const rad = (ang - 90) * Math.PI / 180;
      const ax = 60 + 18 * Math.cos(rad);
      const ay = 25 + 18 * Math.sin(rad);
      return `<rect x="10" y="10" width="70" height="55" rx="6" fill="#1e3a5f" stroke="#0369a1" stroke-width="1.5"/>
        <circle cx="60" cy="25" r="18" fill="#0c4a6e" stroke="#0369a1" stroke-width="1.5"/>
        <circle cx="60" cy="25" r="5" fill="#1d4ed8"/>
        <line x1="60" y1="25" x2="${ax.toFixed(1)}" y2="${ay.toFixed(1)}" stroke="#60a5fa" stroke-width="3" stroke-linecap="round"/>
        <text x="28" y="55" text-anchor="middle" fill="#93c5fd" font-size="7">SERVO</text>
        <text x="28" y="65" text-anchor="middle" fill="#60a5fa" font-size="7">${ang}°</text>
        <line x1="0" y1="25" x2="10" y2="25" stroke="#60a5fa" stroke-width="1.5"/>
        <line x1="0" y1="40" x2="10" y2="40" stroke="#60a5fa" stroke-width="1.5"/>
        <line x1="0" y1="55" x2="10" y2="55" stroke="#60a5fa" stroke-width="1.5"/>`;
    }
  },

  dc_motor: {
    name: 'Мотор DC', category: 'actuator', icon: '🔄',
    w: 70, h: 60,
    color: '#374151',
    props: {},
    pins: [
      {id:'p',x:0,y:20,lbl:'+'},{id:'n',x:0,y:40,lbl:'-'},
    ],
    render(c) {
      const on = c._lit;
      return `<circle cx="45" cy="30" r="28" fill="${on?'#1e3a5f':'#1f2937'}" stroke="#374151" stroke-width="2"/>
        <circle cx="45" cy="30" r="18" fill="${on?'#1d4ed8':'#374151'}" stroke="#4b5563" stroke-width="1.5"/>
        ${on?`<text x="45" y="35" text-anchor="middle" fill="#93c5fd" font-size="16">↻</text>`
            :`<text x="45" y="35" text-anchor="middle" fill="#6b7280" font-size="10">DC</text>`}
        <line x1="0" y1="20" x2="17" y2="20" stroke="#9ca3af" stroke-width="2"/>
        <line x1="0" y1="40" x2="17" y2="40" stroke="#9ca3af" stroke-width="2"/>
        <text x="45" y="58" text-anchor="middle" fill="#6b7280" font-size="7">Motor</text>`;
    }
  },

  relay: {
    name: 'Реле', category: 'actuator', icon: '🔀',
    w: 90, h: 80,
    color: '#1e40af',
    props: {type: '5V'},
    pins: [
      {id:'vcc',x:0,y:20,lbl:'VCC',type:'vcc'},
      {id:'gnd',x:0,y:35,lbl:'GND',type:'gnd'},
      {id:'in', x:0,y:50,lbl:'IN'},
      {id:'com',x:90,y:20,lbl:'COM'},
      {id:'no', x:90,y:40,lbl:'NO'},
      {id:'nc', x:90,y:60,lbl:'NC'},
    ],
    render(c) {
      return `<rect x="8" y="0" width="74" height="80" rx="5" fill="#1e3a5f" stroke="#1e40af" stroke-width="1.5"/>
        <rect x="14" y="6" width="34" height="35" rx="3" fill="#172554" stroke="#3b82f6" stroke-width="1"/>
        <text x="31" y="28" text-anchor="middle" fill="#93c5fd" font-size="8">COIL</text>
        <rect x="52" y="6" width="24" height="68" rx="3" fill="#172554" stroke="#3b82f6" stroke-width="1"/>
        <text x="64" y="38" text-anchor="middle" fill="#93c5fd" font-size="7" transform="rotate(-90,64,38)">RELAY</text>
        <text x="45" y="75" text-anchor="middle" fill="#3b82f6" font-size="7">${c.props.type||'5V'}</text>
        <line x1="0" y1="20" x2="8" y2="20" stroke="#3b82f6" stroke-width="1.5"/>
        <line x1="0" y1="35" x2="8" y2="35" stroke="#3b82f6" stroke-width="1.5"/>
        <line x1="0" y1="50" x2="8" y2="50" stroke="#3b82f6" stroke-width="1.5"/>
        <line x1="82" y1="20" x2="90" y2="20" stroke="#3b82f6" stroke-width="1.5"/>
        <line x1="82" y1="40" x2="90" y2="40" stroke="#3b82f6" stroke-width="1.5"/>
        <line x1="82" y1="60" x2="90" y2="60" stroke="#3b82f6" stroke-width="1.5"/>`;
    }
  },

  // ── ICs & Modules ─────────────────────────────────────────────────────────
  ne555: {
    name: 'Таймер NE555', category: 'ic', icon: '⏱',
    w: 80, h: 110,
    color: '#525252',
    props: {mode: 'astable'},
    pins: [
      {id:'gnd',   x:0,y:20,lbl:'1 GND',type:'gnd'},
      {id:'trig',  x:0,y:38,lbl:'2 TRIG'},
      {id:'out',   x:0,y:56,lbl:'3 OUT'},
      {id:'rst',   x:0,y:74,lbl:'4 RST'},
      {id:'cv',    x:80,y:20,lbl:'5 CV'},
      {id:'thres', x:80,y:38,lbl:'6 THR'},
      {id:'dis',   x:80,y:56,lbl:'7 DIS'},
      {id:'vcc',   x:80,y:74,lbl:'8 VCC',type:'vcc'},
    ],
    render(c) {
      return `<rect x="10" y="0" width="60" height="110" rx="4" fill="#292524" stroke="#525252" stroke-width="2"/>
        <rect x="10" y="0" width="60" height="14" rx="4" fill="none"/>
        <path d="M34,0 Q40,6 46,0" fill="#1c1917" stroke="#525252" stroke-width="1.5"/>
        <text x="40" y="50" text-anchor="middle" fill="#d6d3d1" font-size="8" font-weight="bold">NE555</text>
        <text x="40" y="63" text-anchor="middle" fill="#a8a29e" font-size="7">${c.props.mode||''}</text>
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="10" y2="${p.y}" stroke="#a8a29e" stroke-width="1.5"/>
          <text x="12" y="${p.y+3}" fill="#a8a29e" font-size="6">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===80).map(p=>`
          <line x1="70" y1="${p.y}" x2="80" y2="${p.y}" stroke="#a8a29e" stroke-width="1.5"/>
          <text x="68" y="${p.y+3}" text-anchor="end" fill="#a8a29e" font-size="6">${p.lbl}</text>
        `).join('')}`;
    }
  },

  l298n: {
    name: 'L298N (мотор-драйвер)', category: 'ic', icon: '🚗',
    w: 130, h: 120,
    color: '#0f766e',
    props: {},
    pins: [
      {id:'in1',x:0,y:20,lbl:'IN1'},{id:'in2',x:0,y:35,lbl:'IN2'},
      {id:'in3',x:0,y:55,lbl:'IN3'},{id:'in4',x:0,y:70,lbl:'IN4'},
      {id:'ena',x:0,y:90,lbl:'ENA'},{id:'enb',x:0,y:105,lbl:'ENB'},
      {id:'vcc',x:130,y:20,lbl:'VCC',type:'vcc'},{id:'gnd',x:130,y:40,lbl:'GND',type:'gnd'},
      {id:'5vout',x:130,y:60,lbl:'+5V Out'},
      {id:'outa1',x:130,y:80,lbl:'OUT A1'},{id:'outa2',x:130,y:100,lbl:'OUT A2'},
      {id:'outb1',x:0,y:110,lbl:'OUT B1'},{id:'outb2',x:130,y:115,lbl:'OUT B2'},
    ],
    render() {
      return `<rect x="8" y="0" width="114" height="120" rx="5" fill="#064e3b" stroke="#0f766e" stroke-width="2"/>
        <rect x="20" y="20" width="90" height="80" rx="4" fill="#022c22" stroke="#059669" stroke-width="1"/>
        <text x="65" y="55" text-anchor="middle" fill="#6ee7b7" font-size="10" font-weight="bold">L298N</text>
        <text x="65" y="70" text-anchor="middle" fill="#34d399" font-size="8">Motor Driver</text>
        ${[20,35,55,70,90,105].map(y=>`<line x1="0" y1="${y}" x2="8" y2="${y}" stroke="#34d399" stroke-width="1.5"/>`).join('')}
        ${[20,40,60,80,100,115].map(y=>`<line x1="122" y1="${y}" x2="130" y2="${y}" stroke="#34d399" stroke-width="1.5"/>`).join('')}
        <line x1="0" y1="110" x2="8" y2="110" stroke="#34d399" stroke-width="1.5"/>`;
    }
  },

  shift_reg_595: {
    name: '74HC595 (сдвиговый рег.)', category: 'ic', icon: '≫',
    w: 100, h: 140,
    color: '#374151',
    props: {},
    pins: [
      {id:'qa',  x:0,y:20,lbl:'1 QA'}, {id:'qb',  x:0,y:34,lbl:'2 QB'},
      {id:'qc',  x:0,y:48,lbl:'3 QC'}, {id:'qd',  x:0,y:62,lbl:'4 QD'},
      {id:'qe',  x:0,y:76,lbl:'5 QE'}, {id:'qf',  x:0,y:90,lbl:'6 QF'},
      {id:'qg',  x:0,y:104,lbl:'7 QG'},{id:'gnd',  x:0,y:118,lbl:'8 GND',type:'gnd'},
      {id:'qh2', x:100,y:20,lbl:'9 QH\''},{id:'srclr',x:100,y:34,lbl:'10 SRCLR'},
      {id:'srclk',x:100,y:48,lbl:'11 SRCLK'},{id:'rclk',x:100,y:62,lbl:'12 RCLK'},
      {id:'oe',   x:100,y:76,lbl:'13 OE'}, {id:'ser',   x:100,y:90,lbl:'14 SER'},
      {id:'qh',   x:100,y:104,lbl:'15 QH'},{id:'vcc',   x:100,y:118,lbl:'16 VCC',type:'vcc'},
    ],
    render() {
      return `<rect x="14" y="0" width="72" height="140" rx="4" fill="#1f2937" stroke="#374151" stroke-width="2"/>
        <path d="M40,0 Q50,7 60,0" fill="#111827" stroke="#374151" stroke-width="1.5"/>
        <text x="50" y="62" text-anchor="middle" fill="#d1d5db" font-size="7" font-weight="bold">74HC595</text>
        <text x="50" y="74" text-anchor="middle" fill="#9ca3af" font-size="6">Shift Reg.</text>
        ${[20,34,48,62,76,90,104,118].map(y=>`<line x1="0" y1="${y}" x2="14" y2="${y}" stroke="#6b7280" stroke-width="1.5"/>`).join('')}
        ${[20,34,48,62,76,90,104,118].map(y=>`<line x1="86" y1="${y}" x2="100" y2="${y}" stroke="#6b7280" stroke-width="1.5"/>`).join('')}`;
    }
  },

  // ── Connectors & Misc ─────────────────────────────────────────────────────
  breadboard_mini: {
    name: 'Мини-макетная плата', category: 'passive', icon: '⬜',
    w: 160, h: 80,
    color: '#d97706',
    props: {},
    pins: [
      {id:'r1c1',x:20,y:0,lbl:''},{id:'r1c2',x:40,y:0,lbl:''},{id:'r1c3',x:60,y:0,lbl:''},
      {id:'r1c4',x:80,y:0,lbl:''},{id:'r1c5',x:100,y:0,lbl:''},{id:'r1c6',x:120,y:0,lbl:''},
      {id:'r2c1',x:20,y:80,lbl:''},{id:'r2c2',x:40,y:80,lbl:''},{id:'r2c3',x:60,y:80,lbl:''},
      {id:'r2c4',x:80,y:80,lbl:''},{id:'r2c5',x:100,y:80,lbl:''},{id:'r2c6',x:120,y:80,lbl:''},
    ],
    render() {
      let holes = '';
      for (let row = 0; row < 6; row++) {
        for (let col = 0; col < 6; col++) {
          holes += `<circle cx="${20 + col*24}" cy="${16 + row*10}" r="2.5" fill="#78350f" stroke="#92400e" stroke-width="0.5"/>`;
          holes += `<circle cx="${20 + col*24}" cy="${54 + row*10}" r="2.5" fill="#78350f" stroke="#92400e" stroke-width="0.5"/>`;
        }
      }
      return `<rect x="0" y="0" width="160" height="80" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <rect x="4" y="4" width="152" height="33" rx="3" fill="#fde68a"/>
        <rect x="4" y="43" width="152" height="33" rx="3" fill="#fde68a"/>
        ${holes}`;
    }
  },
};

// Порядок в палитре
const PALETTE_ORDER = [
  ['mcu',        'Микроконтроллеры'],
  ['power',      'Питание'],
  ['passive',    'Пассивные элементы'],
  ['transistor', 'Транзисторы'],
  ['gate',       'Логические вентили'],
  ['sensor',     'Датчики'],
  ['display',    'Дисплеи'],
  ['actuator',   'Актуаторы'],
  ['ic',         'ИС / Модули'],
];


// ── Утилиты ──────────────────────────────────────────────────────────────────

let _idSeq = 0;
const uid = () => `c${++_idSeq}_${Date.now().toString(36)}`;
const snap = (v, g) => Math.round(v / g) * g;
const dist2 = (x1,y1,x2,y2) => (x2-x1)**2+(y2-y1)**2;

function absPin(comp, pin) {
  return {x: comp.x + pin.x, y: comp.y + pin.y};
}


// ── Состояние схемы ───────────────────────────────────────────────────────────

class CircuitState {
  constructor() {
    this.components = [];  // {id, type(key), x, y, props, _lit, _pressed}
    this.wires = [];       // {id, from:{compId,pinId}, to:{compId,pinId}, pts:[{x,y},...]}
  }

  addComponent(typeKey, x, y) {
    const t = CT[typeKey];
    if (!t) return null;
    const c = {
      id: uid(), typeKey,
      type: t,           // reference to type definition
      x, y,
      w: t.w, h: t.h,
      props: {...(t.props||{})},
      _lit: false, _pressed: false,
    };
    this.components.push(c);
    this.simulate();
    return c;
  }

  removeComponent(id) {
    this.components = this.components.filter(c => c.id !== id);
    this.wires = this.wires.filter(w => w.from.compId !== id && w.to.compId !== id);
    this.simulate();
  }

  addWire(fromCompId, fromPinId, toCompId, toPinId) {
    if (fromCompId === toCompId) return null;
    const dup = this.wires.find(w =>
      (w.from.compId===fromCompId && w.from.pinId===fromPinId &&
       w.to.compId===toCompId   && w.to.pinId===toPinId) ||
      (w.to.compId===fromCompId && w.to.pinId===fromPinId &&
       w.from.compId===toCompId && w.from.pinId===toPinId)
    );
    if (dup) return null;
    const wire = {
      id: uid(),
      from: {compId: fromCompId, pinId: fromPinId},
      to:   {compId: toCompId,   pinId: toPinId},
    };
    this.wires.push(wire);
    this.simulate();
    return wire;
  }

  removeWire(id) {
    this.wires = this.wires.filter(w => w.id !== id);
    this.simulate();
  }

  getComp(id) { return this.components.find(c => c.id === id); }

  getPin(comp, pinId) {
    if (!comp) return null;
    return comp.type.pins.find(p => p.id === pinId);
  }

  // Строим граф смежности для симуляции
  simulate() {
    // Сброс состояния
    this.components.forEach(c => { c._lit = false; });

    // Граф: каждый пин — вершина; рёбра — провода
    // Ищем VCC-источники и GND
    const nodes = new Map(); // "${compId}:${pinId}" → Set(соседей)
    const key = (cid,pid) => `${cid}:${pid}`;

    for (const c of this.components) {
      for (const p of c.type.pins) {
        nodes.set(key(c.id,p.id), new Set());
      }
    }
    for (const w of this.wires) {
      const k1 = key(w.from.compId, w.from.pinId);
      const k2 = key(w.to.compId, w.to.pinId);
      if (nodes.has(k1)) nodes.get(k1).add(k2);
      if (nodes.has(k2)) nodes.get(k2).add(k1);
    }

    // BFS от всех VCC-источников
    const vccNodes = new Set();
    for (const c of this.components) {
      for (const p of c.type.pins) {
        if (p.type === 'vcc' || c.typeKey === 'vcc') {
          vccNodes.add(key(c.id, p.id));
        }
      }
    }
    const gndNodes = new Set();
    for (const c of this.components) {
      for (const p of c.type.pins) {
        if (p.type === 'gnd' || c.typeKey === 'gnd') {
          gndNodes.add(key(c.id, p.id));
        }
      }
    }

    // Обходим связные компоненты графа
    // Узел «заряжен» если достижим из VCC
    const charged = new Set([...vccNodes]);
    let changed = true;
    while (changed) {
      changed = false;
      for (const [node, nbrs] of nodes) {
        if (charged.has(node)) {
          for (const nb of nbrs) {
            if (!charged.has(nb)) { charged.add(nb); changed = true; }
          }
        }
      }
    }

    // Helper: is a pin node connected to GND network?
    const isGnd = (nodeKey) => {
      if (gndNodes.has(nodeKey)) return true;
      return [...(nodes.get(nodeKey)||[])].some(n => gndNodes.has(n));
    };
    // Helper: is a pin node charged (connected to VCC network)?
    const isPwr = (nodeKey) => charged.has(nodeKey);

    for (const c of this.components) {
      if (c.typeKey === 'led') {
        c._lit = isPwr(key(c.id,'anode')) && isGnd(key(c.id,'cathode'));
      }
      if (c.typeKey === 'buzzer') {
        c._lit = isPwr(key(c.id,'p')) && isGnd(key(c.id,'n'));
      }
      if (c.typeKey === 'dc_motor') {
        c._lit = (isPwr(key(c.id,'p')) && isGnd(key(c.id,'n')))
               || (isPwr(key(c.id,'n')) && isGnd(key(c.id,'p')));
      }
      if (c.typeKey === 'relay') {
        // Coil energised: VCC + IN charged, GND connected
        c._lit = isPwr(key(c.id,'in')) && isPwr(key(c.id,'vcc')) && isGnd(key(c.id,'gnd'));
      }
    }
  }

  toJSON() {
    return JSON.stringify({
      components: this.components.map(c => ({
        id: c.id, typeKey: c.typeKey,
        x: c.x, y: c.y, props: c.props
      })),
      wires: this.wires.map(w => ({
        id: w.id,
        from: w.from, to: w.to
      }))
    }, null, 2);
  }

  fromJSON(json) {
    const data = typeof json === 'string' ? JSON.parse(json) : json;
    this.components = [];
    this.wires = [];
    for (const cd of (data.components||[])) {
      const t = CT[cd.typeKey];
      if (!t) continue;
      this.components.push({
        id: cd.id, typeKey: cd.typeKey, type: t,
        x: cd.x, y: cd.y,
        w: t.w, h: t.h,
        props: {...(t.props||{}), ...cd.props},
        _lit: false, _pressed: false,
      });
    }
    for (const wd of (data.wires||[])) {
      this.wires.push({id: wd.id, from: wd.from, to: wd.to});
    }
    this.simulate();
  }
}


// ── Редактор (UI) ─────────────────────────────────────────────────────────────

class CircuitEditor {
  constructor(svgEl, state, opts={}) {
    this.svg   = svgEl;
    this.state = state;
    this.opts  = opts; // {onSave, onSubmit, readonly}
    this.GRID  = 20;
    this.selected = null;  // {type:'comp'|'wire', id}
    this.mode  = 'select'; // 'select' | 'add:<typeKey>' | 'wire'
    this.wire  = null;     // {fromCompId, fromPinId, x1, y1, curX, curY}
    this.drag  = null;     // {compId, ox, oy, mx, my}
    this.vb    = {x:0, y:0, w:1400, h:900}; // viewBox
    this.history = [];   // undo stack (JSON strings)
    this.redoStack = [];

    this._setupSVG();
    this._setupEvents();
    this.render();
  }

  // ── SVG setup ────────────────────────────────────────────────────────────

  _setupSVG() {
    this.svg.setAttribute('width',  '100%');
    this.svg.setAttribute('height', '100%');
    this._applyVB();

    // Слои
    this._layerGrid  = this._mkLayer('layer-grid');
    this._layerWires = this._mkLayer('layer-wires');
    this._layerComps = this._mkLayer('layer-comps');
    this._layerUI    = this._mkLayer('layer-ui');

    this._drawGrid();
  }

  _mkLayer(id) {
    let g = document.getElementById(id);
    if (!g) {
      g = document.createElementNS('http://www.w3.org/2000/svg','g');
      g.id = id;
      this.svg.appendChild(g);
    }
    return g;
  }

  _applyVB() {
    this.svg.setAttribute('viewBox',
      `${this.vb.x} ${this.vb.y} ${this.vb.w} ${this.vb.h}`);
  }

  _drawGrid() {
    const g = this.GRID;
    const W = 4000, H = 4000;
    let html = `<defs>
      <pattern id="smallGrid" width="${g}" height="${g}" patternUnits="userSpaceOnUse">
        <path d="M ${g} 0 L 0 0 0 ${g}" fill="none" stroke="var(--grid-color,#e5e7eb)" stroke-width="0.5"/>
      </pattern>
      <pattern id="bigGrid" width="${g*5}" height="${g*5}" patternUnits="userSpaceOnUse">
        <rect width="${g*5}" height="${g*5}" fill="url(#smallGrid)"/>
        <path d="M ${g*5} 0 L 0 0 0 ${g*5}" fill="none" stroke="var(--grid-color2,#d1d5db)" stroke-width="1"/>
      </pattern>
    </defs>
    <rect width="${W}" height="${H}" fill="url(#bigGrid)"/>`;
    this._layerGrid.innerHTML = html;
  }


  // ── Рендер ───────────────────────────────────────────────────────────────

  render() {
    this._renderWires();
    this._renderComps();
    this._renderUI();
    this._notifyChange();
  }

  _renderWires() {
    const html = this.state.wires.map(w => {
      const fc = this.state.getComp(w.from.compId);
      const tc = this.state.getComp(w.to.compId);
      if (!fc||!tc) return '';
      const fp = this.state.getPin(fc, w.from.pinId);
      const tp = this.state.getPin(tc, w.to.pinId);
      if (!fp||!tp) return '';
      const {x:x1,y:y1} = absPin(fc,fp);
      const {x:x2,y:y2} = absPin(tc,tp);
      const sel = this.selected?.type==='wire'&&this.selected.id===w.id;
      // Manhattan routing
      const mx = x1 + (x2-x1)/2;
      const path = `M${x1},${y1} L${mx},${y1} L${mx},${y2} L${x2},${y2}`;
      return `<path id="wire-${w.id}" d="${path}"
        fill="none" stroke="${sel?'#f59e0b':'#374151'}" stroke-width="${sel?3:2}"
        stroke-linecap="round" cursor="pointer"
        data-wire="${w.id}"/>`;
    }).join('');
    this._layerWires.innerHTML = html;
  }

  _renderComps() {
    const html = this.state.components.map(c => {
      const sel = this.selected?.type==='comp'&&this.selected.id===c.id;
      const selRect = sel
        ? `<rect x="-4" y="-4" width="${c.w+8}" height="${c.h+8}" rx="5"
              fill="none" stroke="#667eea" stroke-width="2" stroke-dasharray="5,3" opacity="0.8"/>`
        : '';
      const pins = c.type.pins.map(p => {
        const {x,y} = absPin(c,p);
        const hover = (this.mode.startsWith('wire') && this.wire)
          ? `<circle cx="${p.x}" cy="${p.y}" r="6" fill="#667eea" opacity="0.25" class="pin-hover"/>`
          : '';
        return `<g class="pin" data-comp="${c.id}" data-pin="${p.id}" cursor="crosshair">
          ${hover}
          <circle cx="${p.x}" cy="${p.y}" r="4" fill="#fff" stroke="${sel?'#667eea':'#9ca3af'}"
            stroke-width="1.5" class="pin-dot"/>
        </g>`;
      }).join('');
      return `<g id="comp-${c.id}" class="circuit-comp" transform="translate(${c.x},${c.y})"
              data-comp="${c.id}" cursor="${this.opts.readonly?'default':'move'}">
        ${selRect}
        ${c.type.render(c)}
        ${pins}
      </g>`;
    }).join('');
    this._layerComps.innerHTML = html;
  }

  _renderUI() {
    if (this.wire) {
      const x1=this.wire.x1, y1=this.wire.y1, x2=this.wire.curX||x1, y2=this.wire.curY||y1;
      const mx=x1+(x2-x1)/2;
      this._layerUI.innerHTML =
        `<path d="M${x1},${y1} L${mx},${y1} L${mx},${y2} L${x2},${y2}"
          fill="none" stroke="#667eea" stroke-width="2" stroke-dasharray="6,3"/>`;
    } else {
      this._layerUI.innerHTML = '';
    }
  }


  // ── События ───────────────────────────────────────────────────────────────

  _setupEvents() {
    if (this.opts.readonly) return;

    this.svg.addEventListener('mousedown', e => this._onMouseDown(e));
    this.svg.addEventListener('mousemove', e => this._onMouseMove(e));
    this.svg.addEventListener('mouseup',   e => this._onMouseUp(e));
    this.svg.addEventListener('wheel',     e => this._onWheel(e), {passive:false});
    window.addEventListener('keydown',     e => this._onKey(e));
    this.svg.addEventListener('contextmenu', e => {
      e.preventDefault();
      this._cancelMode();
    });
  }

  _svgCoords(e) {
    const pt = this.svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    const m = this.svg.getScreenCTM().inverse();
    const r = pt.matrixTransform(m);
    return {x: r.x, y: r.y};
  }

  _onMouseDown(e) {
    if (e.button !== 0) return;
    const {x,y} = this._svgCoords(e);

    // Клик по пину → начать или закончить провод
    const pinEl = e.target.closest('.pin');
    if (pinEl) {
      e.stopPropagation();
      const compId = pinEl.dataset.comp;
      const pinId  = pinEl.dataset.pin;
      const comp   = this.state.getComp(compId);
      const pin    = this.state.getPin(comp, pinId);
      if (!comp||!pin) return;
      const {x:px,y:py} = absPin(comp,pin);

      if (this.wire) {
        // Завершить провод
        if (compId !== this.wire.fromCompId) {
          this._pushHistory();
          this.state.addWire(this.wire.fromCompId, this.wire.fromPinId, compId, pinId);
        }
        this.wire = null;
        this.mode = 'select';
      } else {
        // Начать провод
        this.wire = {fromCompId:compId, fromPinId:pinId, x1:px, y1:py, curX:px, curY:py};
        this.mode = 'wire';
        this.selected = null;
      }
      this.render();
      return;
    }

    // Клик по проводу → выделить
    const wireEl = e.target.closest('[data-wire]');
    if (wireEl) {
      this.selected = {type:'wire', id: wireEl.dataset.wire};
      this._cancelMode();
      this.render();
      return;
    }

    // Клик по компоненту → выделить + начать перетаскивание
    const compEl = e.target.closest('.circuit-comp');
    if (compEl) {
      const compId = compEl.dataset.comp;
      this.selected = {type:'comp', id:compId};
      const comp = this.state.getComp(compId);
      if (comp) {
        this.drag = {compId, ox:comp.x, oy:comp.y, mx:x, my:y};
      }
      this._cancelMode();
      this.render();
      return;
    }

    // Клик в режиме добавления компонента
    if (this.mode.startsWith('add:')) {
      const typeKey = this.mode.slice(4);
      this._pushHistory();
      const sx = snap(x, this.GRID);
      const sy = snap(y, this.GRID);
      const c = this.state.addComponent(typeKey, sx, sy);
      this.selected = {type:'comp', id:c.id};
      this.render();
      return;
    }

    // Клик на пустом месте — снять выделение
    this.selected = null;
    this._cancelMode();
    this.render();
  }

  _onMouseMove(e) {
    const {x,y} = this._svgCoords(e);

    if (this.drag) {
      const comp = this.state.getComp(this.drag.compId);
      if (comp) {
        comp.x = snap(this.drag.ox + (x - this.drag.mx), this.GRID);
        comp.y = snap(this.drag.oy + (y - this.drag.my), this.GRID);
        this.state.simulate();
        this.render();
      }
      return;
    }

    if (this.wire) {
      this.wire.curX = x;
      this.wire.curY = y;
      this._renderUI();
      return;
    }

    // Pan if space is held
    if (this._panning) {
      this.vb.x -= (x - this._panStart.x);
      this.vb.y -= (y - this._panStart.y);
      this._applyVB();
    }
  }

  _onMouseUp(e) {
    if (this.drag) {
      this._pushHistory();
      this.drag = null;
    }
    this._panning = false;
  }

  _onWheel(e) {
    e.preventDefault();
    const {x,y} = this._svgCoords(e);
    const factor = e.deltaY > 0 ? 1.15 : 0.87;
    this.vb.x = x - (x - this.vb.x) * factor;
    this.vb.y = y - (y - this.vb.y) * factor;
    this.vb.w *= factor;
    this.vb.h *= factor;
    this._applyVB();
  }

  _onKey(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'Escape') { this._cancelMode(); this.render(); }

    if ((e.key === 'Delete' || e.key === 'Backspace') && this.selected) {
      this._pushHistory();
      if (this.selected.type === 'comp') this.state.removeComponent(this.selected.id);
      if (this.selected.type === 'wire') this.state.removeWire(this.selected.id);
      this.selected = null;
      this.render();
    }

    if ((e.ctrlKey||e.metaKey) && e.key === 'z') { e.preventDefault(); this.undo(); }
    if ((e.ctrlKey||e.metaKey) && e.key === 'y') { e.preventDefault(); this.redo(); }
    if ((e.ctrlKey||e.metaKey) && e.key === 's') { e.preventDefault(); this.save(); }
  }


  // ── История (undo/redo) ───────────────────────────────────────────────────

  _pushHistory() {
    this.history.push(this.state.toJSON());
    if (this.history.length > 50) this.history.shift();
    this.redoStack = [];
  }

  undo() {
    if (!this.history.length) return;
    this.redoStack.push(this.state.toJSON());
    this.state.fromJSON(this.history.pop());
    this.selected = null;
    this.render();
  }

  redo() {
    if (!this.redoStack.length) return;
    this.history.push(this.state.toJSON());
    this.state.fromJSON(this.redoStack.pop());
    this.selected = null;
    this.render();
  }


  // ── Режимы ────────────────────────────────────────────────────────────────

  startAdd(typeKey) {
    this._cancelMode();
    this.mode = `add:${typeKey}`;
    this.svg.style.cursor = 'crosshair';
    this._updateStatus(`Кликни на схему чтобы разместить ${CT[typeKey]?.name}`);
  }

  _cancelMode() {
    this.wire = null;
    if (this.mode !== 'select') {
      this.mode = 'select';
      this.svg.style.cursor = '';
      this._updateStatus('');
    }
  }

  startWireMode() {
    this._cancelMode();
    this.mode = 'wire';
    this.svg.style.cursor = 'crosshair';
    this._updateStatus('Кликни на пин компонента чтобы начать провод');
  }


  // ── Сохранение ───────────────────────────────────────────────────────────

  save() {
    if (this.opts.onSave) this.opts.onSave(this.state.toJSON());
  }

  submit() {
    if (this.opts.onSubmit) this.opts.onSubmit(this.state.toJSON());
  }

  clear() {
    this._pushHistory();
    this.state.components = [];
    this.state.wires = [];
    this.selected = null;
    this.render();
  }

  fitView() {
    if (!this.state.components.length) {
      this.vb = {x:0,y:0,w:1400,h:900};
    } else {
      const xs = this.state.components.map(c => c.x);
      const ys = this.state.components.map(c => c.y);
      const x2 = this.state.components.map(c => c.x + c.w);
      const y2 = this.state.components.map(c => c.y + c.h);
      const pad = 60;
      this.vb = {
        x: Math.min(...xs)-pad, y: Math.min(...ys)-pad,
        w: Math.max(...x2)-Math.min(...xs)+pad*2,
        h: Math.max(...y2)-Math.min(...ys)+pad*2,
      };
    }
    this._applyVB();
  }


  // ── Вспомогательные ──────────────────────────────────────────────────────

  _updateStatus(msg) {
    const el = document.getElementById('circuit-status');
    if (el) el.textContent = msg;
  }

  _notifyChange() {
    const el = document.getElementById('circuit-json-hidden');
    if (el) el.value = this.state.toJSON();
  }

  updateProp(propKey, value) {
    if (!this.selected || this.selected.type !== 'comp') return;
    const comp = this.state.getComp(this.selected.id);
    if (!comp) return;
    this._pushHistory();
    comp.props[propKey] = value;
    this.state.simulate();
    this.render();
    this._renderPropsPanel();
  }

  _renderPropsPanel() {
    const panel = document.getElementById('props-panel');
    if (!panel) return;
    if (!this.selected || this.selected.type !== 'comp') {
      panel.innerHTML = '<p class="props-hint">Выбери компонент чтобы изменить свойства</p>';
      return;
    }
    const comp = this.state.getComp(this.selected.id);
    if (!comp) return;
    let html = `<div class="props-title">${comp.type.name}</div>`;

    if (comp.typeKey === 'resistor') {
      const vals = ['100 Ω','220 Ω','470 Ω','1 kΩ','4.7 kΩ','10 kΩ'];
      html += `<label class="prop-label">Номинал</label>
        <select class="prop-input" onchange="EDITOR.updateProp('value',this.value)">
          ${vals.map(v=>`<option${comp.props.value===v?' selected':''}>${v}</option>`).join('')}
        </select>`;
    }
    if (comp.typeKey === 'led') {
      const colors = ['red','green','yellow','blue','white'];
      html += `<label class="prop-label">Цвет</label>
        <select class="prop-input" onchange="EDITOR.updateProp('color',this.value)">
          ${colors.map(c=>`<option${comp.props.color===c?' selected':''}>${c}</option>`).join('')}
        </select>`;
    }
    html += `<button class="prop-delete-btn" onclick="EDITOR._deleteSelected()">
      <i class="fas fa-trash"></i> Удалить
    </button>`;
    panel.innerHTML = html;
  }

  _deleteSelected() {
    if (!this.selected) return;
    this._pushHistory();
    if (this.selected.type === 'comp') this.state.removeComponent(this.selected.id);
    if (this.selected.type === 'wire') this.state.removeWire(this.selected.id);
    this.selected = null;
    this.render();
    this._renderPropsPanel();
  }

  // Обновляем панель свойств при каждом render
  render() {
    this._renderWires();
    this._renderComps();
    this._renderUI();
    this._notifyChange();
    this._renderPropsPanel();
  }
}


// ── Инициализация ─────────────────────────────────────────────────────────────

let EDITOR = null;

function initCircuitEditor(config) {
  const svgEl = document.getElementById('circuit-svg');
  if (!svgEl) return;

  const state = new CircuitState();

  // Загрузить сохранённую схему
  if (config.initialJson && config.initialJson !== 'null') {
    try { state.fromJSON(config.initialJson); } catch(e) { console.warn('Bad JSON', e); }
  }

  EDITOR = new CircuitEditor(svgEl, state, {
    readonly: config.readonly || false,
    onSave(json) {
      fetch(config.saveUrl, {
        method: 'POST',
        headers: {'Content-Type':'application/json','X-CSRFToken': config.csrf},
        body: json
      }).then(r=>r.json()).then(d=>{
        const msg = document.getElementById('save-msg');
        if (msg) { msg.textContent='✓ Сохранено'; msg.style.opacity=1; setTimeout(()=>msg.style.opacity=0, 2000); }
      }).catch(()=>{});
    },
    onSubmit(json) {
      document.getElementById('circuit-json-hidden').value = json;
      document.getElementById('circuit-submit-form').submit();
    }
  });

  // Палитра
  buildPalette();

  // Сохранение каждые 30 секунд автоматически
  if (!config.readonly) {
    setInterval(()=>EDITOR.save(), 30000);
  }
}

function buildPalette() {
  const container = document.getElementById('palette-container');
  if (!container) return;
  for (const [cat, label] of PALETTE_ORDER) {
    const items = Object.entries(CT).filter(([,t])=>t.category===cat);
    if (!items.length) continue;
    let html = `<div class="palette-group-label">${label}</div>`;
    for (const [key, t] of items) {
      html += `<button class="palette-item" onclick="EDITOR.startAdd('${key}')" title="${t.name}">
        <span class="palette-icon">${t.icon}</span>
        <span class="palette-name">${t.name}</span>
      </button>`;
    }
    container.insertAdjacentHTML('beforeend', html);
  }
}
