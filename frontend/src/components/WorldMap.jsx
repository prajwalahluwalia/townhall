// The archipelago: your island plus the four others it trades with.

const PLACES = {
  you: [120, 150],
  forge: [70, 55],
  aurum: [215, 42],
  petra: [355, 70],
  granara: [355, 200],
}
const STRAIT = [300, 135]

const PARTNER_ICON = {
  petra: (
    <g>
      <path d="M-4,6 L0,-8 L4,6z" fill="none" stroke="#343a40" strokeWidth="1.4" />
      <line x1="-6" y1="-2" x2="6" y2="-2" stroke="#343a40" strokeWidth="1.2" />
      <circle cx="9" cy="3" r="3" fill="#212529" />
    </g>
  ),
  granara: (
    <g stroke="#b08900" strokeWidth="1.6" strokeLinecap="round">
      {[-5, 0, 5].map((x) => <line key={x} x1={x} y1="7" x2={x} y2="-6" />)}
      {[-5, 0, 5].map((x) => <ellipse key={`e${x}`} cx={x} cy="-6" rx="1.8" ry="3" fill="#e9c46a" />)}
    </g>
  ),
  forge: (
    <g>
      <rect x="-8" y="-2" width="16" height="9" fill="#868e96" />
      <rect x="3" y="-10" width="3" height="10" fill="#495057" />
      <circle cx="5" cy="-13" r="2.5" fill="#ced4da" className="smoke" />
    </g>
  ),
  aurum: (
    <g>
      <circle r="8" fill="#fcc419" stroke="#e67700" strokeWidth="1.4" />
      <text y="3.5" textAnchor="middle" fontSize="10" fontWeight="800" fill="#e67700">$</text>
    </g>
  ),
}

function Blob({ x, y, r, fill }) {
  return (
    <path
      d={`M${x - r},${y} q${r * 0.2},${-r * 0.8} ${r},${-r * 0.7} q${r * 0.9},${-r * 0.1} ${r},${r * 0.6} q${-r * 0.1},${r * 0.8} ${-r},${r * 0.6} q${-r * 0.8},${0} ${-r},${-r * 0.5}z`}
      fill={fill}
      stroke="#e9c46a"
      strokeWidth="1.5"
    />
  )
}

export default function WorldMap({ island, world, atWar = true, stance = null, compact = false }) {
  const route = (from, via) => {
    const [x1, y1] = PLACES[from]
    const [x2, y2] = PLACES.you
    if (via) return `M${x1},${y1} Q${via[0]},${via[1]} ${x2},${y2}`
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - 18
    return `M${x1},${y1} Q${mx},${my} ${x2},${y2}`
  }
  const blocked = (id) => atWar && (id === 'granara' || (id === 'petra' && stance !== 'neutral'))
  return (
    <svg viewBox="0 0 420 250" className={`world-map ${compact ? 'compact' : ''}`} role="img"
      aria-label={`Map: ${island.name} and its trading partners${atWar ? '. Petra and Granara are at war and the strait is closed.' : ''}`}>
      <defs>
        <linearGradient id="wm-sea" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#4cc9f0" />
          <stop offset="1" stopColor="#0f7aa0" />
        </linearGradient>
      </defs>
      <rect width="420" height="250" rx="16" fill="url(#wm-sea)" />
      {[30, 90, 160, 220].map((y, i) => (
        <path key={i} d={`M0,${y} q15,-4 30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0`}
          stroke="#fff" strokeOpacity="0.18" fill="none" className="wave" style={{ animationDelay: `${i * 0.5}s` }} />
      ))}

      {['forge', 'aurum', 'petra', 'granara'].map((id) => (
        <path key={id} d={route(id, id === 'petra' || id === 'granara' ? STRAIT : null)} fill="none"
          stroke={blocked(id) ? '#ff6b6b' : '#fffaf0'} strokeWidth="2" strokeDasharray="5 5"
          className={blocked(id) ? '' : 'route'} opacity={blocked(id) ? 0.9 : 0.75} />
      ))}

      {/* strait */}
      <g transform={`translate(${STRAIT[0]},${STRAIT[1]})`}>
        <path d="M-6,-28 q8,10 0,22 M6,28 q-8,-10 0,-22" stroke="#a98c5a" strokeWidth="7" fill="none" strokeLinecap="round" />
        {atWar && (
          <g className="pulse">
            <circle r="13" fill="#ff6b6b" opacity="0.3" />
            <path d="M-6,-6 L6,6 M6,-6 L-6,6" stroke="#c92a2a" strokeWidth="3" strokeLinecap="round" />
          </g>
        )}
        {!compact && <text y="44" textAnchor="middle" className="map-label small">Strait of Teeth</text>}
      </g>

      {atWar && (
        <g transform="translate(372,135)">
          <g className="pulse"><text textAnchor="middle" fontSize="18">⚔️</text></g>
        </g>
      )}

      {Object.entries(PLACES).filter(([id]) => id !== 'you').map(([id, [x, y]]) => {
        const info = world.find((w) => w.id === id)
        return (
          <g key={id}>
            <Blob x={x} y={y} r={22} fill={atWar && (id === 'petra' || id === 'granara') ? '#e9b8a0' : '#b7d99a'} />
            <g transform={`translate(${x},${y - 2})`}>{PARTNER_ICON[id]}</g>
            <text x={x} y={y + 26} textAnchor="middle" className="map-label">{info?.name}</text>
            {!compact && <text x={x} y={y + 37} textAnchor="middle" className="map-label small">{info?.exports}</text>}
          </g>
        )
      })}

      <g>
        <circle cx={PLACES.you[0]} cy={PLACES.you[1]} r="34" fill="#fff" opacity="0.14" className="pulse" />
        <Blob x={PLACES.you[0]} y={PLACES.you[1]} r={28} fill={island.art.palette[0]} />
        <path d={`M${PLACES.you[0]},${PLACES.you[1] - 24} v-12`} stroke="#343a40" strokeWidth="1.4" />
        <path d={`M${PLACES.you[0]},${PLACES.you[1] - 36} h10 l-3,3 l3,3 h-10z`} fill={island.art.palette[1]} className="flag" />
        <text x={PLACES.you[0]} y={PLACES.you[1] + 34} textAnchor="middle" className="map-label strong">{island.name} (you)</text>
      </g>
    </svg>
  )
}
