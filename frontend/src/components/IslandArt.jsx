import { useId, useMemo } from 'react'

// Deterministic randomness so each island always looks the same.
function seeded(str) {
  let h = 2166136261
  for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619)
  return () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507)
    h = Math.imul(h ^ (h >>> 13), 3266489909)
    return ((h ^= h >>> 16) >>> 0) / 4294967296
  }
}

// Smooth closed blob through points (Catmull-Rom to Bezier).
function blobPath(cx, cy, rx, ry, seed, wobble = 1) {
  const n = 14
  const pts = []
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2
    const r = 1 + wobble * (0.07 * Math.sin(3 * a + seed) + 0.05 * Math.sin(5 * a + seed * 2) + 0.03 * Math.sin(7 * a + seed * 3))
    pts.push([cx + Math.cos(a) * rx * r, cy + Math.sin(a) * ry * r])
  }
  let d = `M${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`
  for (let i = 0; i < n; i++) {
    const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n]
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6]
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6]
    d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`
  }
  return d + 'Z'
}

const SKIES = {
  dawn: ['#ffd6a5', '#fdffb6', '#ffe8cc'],
  noon: ['#74c0fc', '#a5d8ff', '#d0ebff'],
  afternoon: ['#4dabf7', '#a5d8ff', '#e7f5ff'],
  evening: ['#ff8c69', '#ffb88c', '#ffe0b2'],
  night: ['#1b2845', '#274060', '#335c81'],
}

function Palm({ x, y, s = 1, bend = 0 }) {
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <path d={`M0,0 Q${3 + bend},-14 ${2 + bend * 2},-28`} stroke="#8d6e4a" strokeWidth="3" fill="none" strokeLinecap="round" />
      <g transform={`translate(${2 + bend * 2},-28)`} className="sway">
        {[-150, -110, -60, -20, 20].map((a, i) => (
          <path key={i} d="M0,0 q8,-6 16,2 q-8,-2 -16,-2z" fill="#3c9a5f" transform={`rotate(${a + 90})`} />
        ))}
      </g>
    </g>
  )
}

function Person({ x, y, color, mood, delay, sign }) {
  return (
    <g transform={`translate(${x},${y})`}>
      <g className={mood === 'cheer' ? 'jump' : mood === 'boo' ? 'shake' : 'idle'} style={{ animationDelay: `${delay}s` }}>
        {sign && (
          <g>
            <line x1="5" y1="-6" x2="5" y2="-22" stroke="#6b4f2a" strokeWidth="1.2" />
            <rect x="-1" y="-30" width="13" height="9" rx="1" fill="#fff" stroke="#c92a2a" strokeWidth="1" />
            <line x1="1.5" y1="-25.5" x2="9.5" y2="-25.5" stroke="#c92a2a" strokeWidth="1.4" />
          </g>
        )}
        <rect x="-3" y="-6" width="6" height="8" rx="2.5" fill={color} />
        <circle cx="0" cy="-9" r="3" fill="#f1c27d" />
        {mood === 'cheer' && <line x1="-3" y1="-5" x2="-6" y2="-11" stroke={color} strokeWidth="1.6" strokeLinecap="round" />}
      </g>
    </g>
  )
}

function Building({ type, x, y, h, w, palette, rnd, smoke }) {
  if (type === 'towers') {
    return (
      <g>
        <rect x={x} y={y - h} width={w} height={h} fill={palette[2]} />
        <rect x={x + 2} y={y - h + 3} width={w - 4} height={h - 6} fill={palette[0]} opacity="0.85" />
        {Array.from({ length: Math.floor(h / 8) }, (_, i) => (
          <line key={i} x1={x + 2} x2={x + w - 2} y1={y - h + 6 + i * 8} y2={y - h + 6 + i * 8} stroke={palette[2]} strokeWidth="0.8" opacity="0.5" />
        ))}
        <rect x={x + w / 2 - 0.5} y={y - h - 8} width="1" height="8" fill={palette[2]} />
      </g>
    )
  }
  if (type === 'factories') {
    return (
      <g>
        <rect x={x + w - 8} y={y - h - 14} width="5" height={h + 14} fill="#6c757d" />
        <rect x={x} y={y - h} width={w} height={h} fill={palette[1]} />
        <path d={`M${x},${y - h} l${w / 4},-7 v7 l${w / 4},-7 v7 l${w / 4},-7 v7 l${w / 4},-7 v7z`} fill={palette[2]} />
        {smoke > 0 && [0, 1, 2].map((i) => (
          <circle key={i} cx={x + w - 5.5} cy={y - h - 18} r={4 + i} fill="#adb5bd" opacity={0.35 + smoke * 0.4}
            className="smoke" style={{ animationDelay: `${i * 0.9 + rnd}s` }} />
        ))}
      </g>
    )
  }
  if (type === 'town') {
    const wall = ['#fff3bf', '#ffd8a8', '#d3f9d8', '#e5dbff'][Math.floor(rnd * 4)]
    return (
      <g>
        <rect x={x} y={y - h} width={w} height={h} fill={wall} stroke="#c9b18f" strokeWidth="0.6" />
        <path d={`M${x - 2},${y - h} L${x + w / 2},${y - h - 8} L${x + w + 2},${y - h}z`} fill="#e8590c" />
        <rect x={x + w / 2 - 2} y={y - 6} width="4" height="6" fill="#8d6e4a" />
      </g>
    )
  }
  // village and huts: thatched huts
  const broken = type === 'huts' && rnd > 0.65
  return (
    <g>
      {type === 'huts' && <line x1={x + 2} y1={y} x2={x + 2} y2={y + 4} stroke="#6b4f2a" strokeWidth="1.2" />}
      {type === 'huts' && <line x1={x + w - 2} y1={y} x2={x + w - 2} y2={y + 4} stroke="#6b4f2a" strokeWidth="1.2" />}
      <rect x={x} y={y - h * 0.6} width={w} height={h * 0.6} fill="#d4a373" />
      <path d={broken
        ? `M${x - 3},${y - h * 0.6} L${x + w / 2},${y - h - 2} L${x + w * 0.7},${y - h * 0.8} L${x + w + 1},${y - h * 0.55}z`
        : `M${x - 3},${y - h * 0.6} L${x + w / 2},${y - h - 2} L${x + w + 3},${y - h * 0.6}z`}
        fill="#bc8a5f" stroke="#8d6e4a" strokeWidth="0.6" />
      <rect x={x + w / 2 - 2} y={y - 5} width="4" height="5" fill="#6b4f2a" />
    </g>
  )
}

export default function IslandArt({
  island,
  mood = null,
  smoke = 0.5,
  green = false,
  boats = 2,
  sky = null,
  className = '',
  crowd = true,
  title,
  fill = false, // cover its box (cropping the edges) instead of keeping the whole picture visible
}) {
  const uid = useId().replace(/[^a-zA-Z0-9_-]/g, '')
  const art = island.art
  const type = art.buildings
  const palette = art.palette
  const scene = useMemo(() => {
    const rnd = seeded(island.id)
    const seed = rnd() * 10
    const size = art.size
    const rx = 150 * size, ry = 58 * size
    const cx = 200, cy = 190
    const sand = blobPath(cx, cy, rx, ry, seed)
    const grass = blobPath(cx, cy - 6, rx * 0.84, ry * 0.72, seed + 0.4, 1.3)
    const left = [], right = []
    const count = { towers: 5, factories: 4, town: 6, village: 5, huts: 4 }[type]
    const dims = {
      towers: () => [16 + rnd() * 10, 50 + rnd() * 60],
      factories: () => [26 + rnd() * 10, 16 + rnd() * 8],
      town: () => [12 + rnd() * 6, 12 + rnd() * 8],
      village: () => [12 + rnd() * 4, 14 + rnd() * 4],
      huts: () => [11 + rnd() * 3, 13 + rnd() * 3],
    }[type]
    let lx = cx - 38, rxp = cx + 38
    for (let i = 0; i < count; i++) {
      const [w, h] = dims()
      const yJit = 168 + rnd() * 10
      if (i % 2 === 0) {
        lx -= w + 4 + rnd() * 4
        if (lx > cx - rx * 0.8) left.push({ x: lx, y: yJit, w, h, r: rnd() })
      } else {
        if (rxp + w < cx + rx * 0.8) right.push({ x: rxp, y: yJit, w, h, r: rnd() })
        rxp += w + 4 + rnd() * 4
      }
    }
    const palms = Array.from({ length: 5 }, (_, i) => ({
      x: cx + (i - 2) * rx * 0.38 + (rnd() - 0.5) * 20,
      y: cy + ry * 0.45 + rnd() * 8,
      s: 0.6 + rnd() * 0.3,
      bend: type === 'huts' ? 4 : (rnd() - 0.5) * 4,
    }))
    const people = Array.from({ length: 16 }, (_, i) => ({
      x: cx - 34 + (i % 8) * 9.5 + (rnd() - 0.5) * 4,
      y: 206 + Math.floor(i / 8) * 9 + rnd() * 2,
      color: ['#e03131', '#1971c2', '#f08c00', '#2f9e44', '#9c36b5', '#0c8599', '#f76707'][Math.floor(rnd() * 7)],
      delay: rnd() * 0.8,
      sign: rnd() > 0.5,
    }))
    return { sand, grass, left, right, palms, people, rx, ry, cx, cy }
  }, [island.id, art.size, type])

  const skyColors = sky ? SKIES[sky] : null
  const night = sky === 'night'

  return (
    <svg viewBox="0 0 400 280" preserveAspectRatio={fill ? 'xMidYMid slice' : 'xMidYMid meet'}
      className={`island-art ${className}`} role="img" aria-label={title || `${island.name} island`}>
      <defs>
        {skyColors && (
          <linearGradient id={`sky${uid}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={skyColors[0]} />
            <stop offset="0.6" stopColor={skyColors[1]} />
            <stop offset="1" stopColor={skyColors[2]} />
          </linearGradient>
        )}
        <linearGradient id={`sea${uid}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={night ? '#16324f' : '#4cc9f0'} />
          <stop offset="1" stopColor={night ? '#0b1d33' : '#0f7aa0'} />
        </linearGradient>
        <radialGradient id={`shallow${uid}`}>
          <stop offset="0.6" stopColor="#9be7f5" stopOpacity="0.9" />
          <stop offset="1" stopColor="#9be7f5" stopOpacity="0" />
        </radialGradient>
      </defs>

      {skyColors && (
        <g>
          <rect width="400" height="120" fill={`url(#sky${uid})`} />
          {night ? (
            <g>
              <circle cx="320" cy="40" r="14" fill="#fff9db" />
              <circle cx="326" cy="36" r="12" fill={skyColors[0]} />
              {[40, 90, 150, 230, 270, 360].map((x, i) => <circle key={i} cx={x} cy={20 + (i % 3) * 18} r="1.2" fill="#fff" className="twinkle" style={{ animationDelay: `${i * 0.4}s` }} />)}
            </g>
          ) : (
            <circle cx={sky === 'dawn' ? 60 : sky === 'evening' ? 340 : 300} cy={sky === 'noon' ? 34 : 70} r="18" fill={sky === 'evening' ? '#ff6b35' : '#ffe066'} opacity="0.95" />
          )}
          <g className="drift" opacity={night ? 0.25 : 0.85}>
            <ellipse cx="110" cy="40" rx="26" ry="8" fill="#fff" />
            <ellipse cx="128" cy="35" rx="16" ry="8" fill="#fff" />
          </g>
          <rect y="118" width="400" height="162" fill={`url(#sea${uid})`} />
        </g>
      )}
      {!skyColors && <ellipse cx={scene.cx} cy={scene.cy + 4} rx={scene.rx * 1.25} ry={scene.ry * 1.5} fill={`url(#shallow${uid})`} />}

      {/* waves */}
      {skyColors && [150, 240, 262].map((y, i) => (
        <path key={i} className="wave" style={{ animationDelay: `${i * 0.7}s` }}
          d={`M-20,${y} q10,-4 20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0`}
          stroke="#ffffff" strokeOpacity="0.35" fill="none" strokeWidth="1.2" />
      ))}

      {/* boats */}
      {Array.from({ length: boats }, (_, i) => (
        <g key={i} className="bob" style={{ animationDelay: `${i * 0.6}s` }} transform={`translate(${i % 2 ? 340 - i * 12 : 40 + i * 14},${236 + (i % 3) * 10})`}>
          <path d="M-10,0 h20 l-4,5 h-12z" fill="#8d6e4a" />
          <path d="M0,-1 v-14 l9,12z" fill="#fff" />
        </g>
      ))}

      <path d={scene.sand} fill="#f4d58d" stroke="#e9c46a" strokeWidth="2" />
      <path d={scene.grass} fill={type === 'towers' ? '#7fbf7f' : type === 'huts' ? '#9bbf6a' : '#6fbf73'} />

      {type === 'village' && (
        <g opacity="0.9">
          {[0, 1, 2].map((i) => (
            <rect key={i} x={scene.cx + 46 + i * 22} y={194 + (i % 2) * 6} width="20" height="9" fill={i % 2 ? '#e9c46a' : '#a7c957'} transform={`skewX(-20)`} />
          ))}
        </g>
      )}

      {green && (
        <g>
          {[0, 1, 2, 3].map((i) => (
            <path key={i} d={`M${scene.cx - 120 + i * 13},${202 + (i % 2) * 5} l10,0 l-3,-6 l-10,0z`} fill="#1c3d6e" stroke="#74c0fc" strokeWidth="0.6" />
          ))}
          <g transform={`translate(${scene.cx + 118},176)`}>
            <line x1="0" y1="0" x2="0" y2="-30" stroke="#f1f3f5" strokeWidth="2" />
            <g className="spin" style={{ transformOrigin: '0px -30px' }}>
              {[0, 120, 240].map((a) => <line key={a} x1="0" y1="-30" x2="0" y2="-44" stroke="#f1f3f5" strokeWidth="2" transform={`rotate(${a} 0 -30)`} />)}
            </g>
          </g>
        </g>
      )}

      {scene.left.concat(scene.right).sort((a, b) => a.y - b.y).map((b, i) => (
        <Building key={i} type={type} x={b.x} y={b.y} w={b.w} h={b.h} palette={palette} rnd={b.r} smoke={smoke} />
      ))}

      {/* Town Hall */}
      <g transform={`translate(${scene.cx},178)`}>
        <rect x="-26" y="-22" width="52" height="24" fill="#fffaf0" stroke="#c9b18f" />
        {[-20, -10, 0, 10, 20].map((x) => <rect key={x} x={x - 1.5} y="-20" width="3" height="20" fill="#e9dcc3" />)}
        <path d="M-30,-22 L0,-36 L30,-22z" fill={palette[1]} stroke="#c9b18f" />
        <path d="M-9,-33 a9,9 0 0 1 18,0z" fill={palette[0]} />
        <line x1="0" y1="-42" x2="0" y2="-58" stroke="#343a40" strokeWidth="1.2" />
        <path className="flag" d="M0,-58 h12 l-3,3.5 l3,3.5 h-12z" fill={palette[0]} />
        <ellipse cx="0" cy="22" rx="46" ry="11" fill="#e9dcc3" opacity="0.85" />
      </g>

      {crowd && mood && scene.people.map((p, i) => (
        <Person key={i} {...p} mood={mood} sign={mood === 'boo' && p.sign} />
      ))}
      {mood === 'cheer' && crowd && [0, 1, 2, 3, 4, 5].map((i) => (
        <rect key={i} x={scene.cx - 40 + i * 15} y="190" width="3" height="5" fill={['#ff6b6b', '#ffd43b', '#69db7c', '#4dabf7'][i % 4]} className="confetti" style={{ animationDelay: `${i * 0.25}s` }} />
      ))}

      {scene.palms.map((p, i) => <Palm key={i} {...p} />)}

      {night && <rect width="400" height="280" fill="#0b1d33" opacity="0.18" pointerEvents="none" />}
    </svg>
  )
}
