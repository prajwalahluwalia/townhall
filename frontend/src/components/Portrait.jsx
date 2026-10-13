import { useId } from 'react'

// Small illustrated portraits for advisors and citizens.

const LOOKS = {
  diplomat: { bg: '#d0ebff', suit: '#1c3d6e', skin: '#c68642', hair: '#2b1d0e', extra: 'sash' },
  finance: { bg: '#e6fcf5', suit: '#495057', skin: '#f1c27d', hair: '#5c3d1e', extra: 'glasses' },
  banker: { bg: '#fff3bf', suit: '#1d2a3a', skin: '#e0ac69', hair: '#868e96', extra: 'tie' },
  trade: { bg: '#d3f9d8', suit: '#2b8a3e', skin: '#8d5524', hair: '#1a1a1a', extra: 'cap' },
  union: { bg: '#ffe8cc', suit: '#f76707', skin: '#c68642', hair: '#1a1a1a', extra: 'hardhat' },
  ceo: { bg: '#f3f0ff', suit: '#212529', skin: '#ffdbac', hair: '#3b2f2f', extra: 'redtie' },
  planner: { bg: '#e3fafc', suit: '#0c8599', skin: '#e0ac69', hair: '#2b1d0e', extra: 'bun' },
  envoy: { bg: '#d0ebff', suit: '#1971c2', skin: '#8d5524', hair: '#1a1a1a', extra: 'beret' },
  saver: { bg: '#fff0f6', suit: '#c2255c', skin: '#e0ac69', hair: '#ced4da', extra: 'bun' },
  driver: { bg: '#fff9db', suit: '#364fc7', skin: '#c68642', hair: '#1a1a1a', extra: 'cap' },
  farmer: { bg: '#ebfbee', suit: '#5c940d', skin: '#a0662f', hair: '#3b2f2f', extra: 'strawhat' },
  shop: { bg: '#fff4e6', suit: '#d9480f', skin: '#8d5524', hair: '#1a1a1a', extra: 'scarf' },
  worker: { bg: '#e7f5ff', suit: '#1864ab', skin: '#ffdbac', hair: '#a5682a', extra: 'overalls' },
}

export default function Portrait({ kind, size = 64, mood = 60, label }) {
  const clip = `pc${useId().replace(/[^a-zA-Z0-9_-]/g, '')}`
  const L = LOOKS[kind] || LOOKS.finance
  // mouth: smile when mood high, frown when low
  const curve = mood >= 62 ? 5 : mood >= 38 ? 0.5 : -4
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" role="img" aria-label={label || kind} className="portrait">
      <circle cx="50" cy="50" r="48" fill={L.bg} />
      <clipPath id={clip}><circle cx="50" cy="50" r="48" /></clipPath>
      <g clipPath={`url(#${clip})`}>
        <path d="M14,100 Q16,70 50,68 Q84,70 86,100z" fill={L.suit} />
        {L.extra === 'overalls' && <rect x="38" y="72" width="24" height="30" rx="3" fill="#74c0fc" />}
        {(L.extra === 'tie' || L.extra === 'redtie') && (
          <>
            <path d="M42,68 L50,80 L58,68z" fill="#fff" />
            <path d="M48,72 h4 l2,20 l-4,5 l-4,-5z" fill={L.extra === 'tie' ? '#f59f00' : '#e03131'} />
          </>
        )}
        {L.extra === 'sash' && <path d="M30,74 L70,100 L62,100 L26,80z" fill="#e03131" />}
        {L.extra === 'scarf' && <path d="M30,46 Q50,20 70,46 L74,78 Q50,88 26,78z" fill="#f08c00" />}
        <rect x="44" y="58" width="12" height="12" fill={L.skin} />
        <circle cx="50" cy="44" r="19" fill={L.skin} />
        {L.extra !== 'scarf' && <path d="M31,42 Q32,22 50,23 Q68,22 69,42 Q62,32 50,32 Q38,32 31,42z" fill={L.hair} />}
        {L.extra === 'bun' && <circle cx="50" cy="22" r="7" fill={L.hair} />}
        <circle cx="43" cy="44" r="2.2" fill="#1d2a3a" />
        <circle cx="57" cy="44" r="2.2" fill="#1d2a3a" />
        {L.extra === 'glasses' && (
          <g fill="none" stroke="#1d2a3a" strokeWidth="1.6">
            <circle cx="43" cy="44" r="5" /><circle cx="57" cy="44" r="5" /><line x1="48" y1="44" x2="52" y2="44" />
          </g>
        )}
        <path d={`M43,54 Q50,${54 + curve} 57,54`} stroke="#7a3e2b" strokeWidth="2.2" fill="none" strokeLinecap="round" />
        {L.extra === 'hardhat' && <path d="M29,36 Q30,18 50,18 Q70,18 71,36 h4 v4 h-50 v-4z" fill="#fcc419" />}
        {L.extra === 'cap' && <path d="M31,34 Q32,20 50,20 Q66,20 69,34 h12 v3 h-50z" fill={kind === 'driver' ? '#212529' : '#2b8a3e'} />}
        {L.extra === 'strawhat' && <><ellipse cx="50" cy="31" rx="30" ry="6" fill="#e9c46a" /><path d="M36,31 Q38,15 50,15 Q62,15 64,31z" fill="#e9c46a" /><rect x="36" y="27" width="28" height="3" fill="#c92a2a" /></>}
        {L.extra === 'beret' && <path d="M30,32 Q34,16 54,18 Q72,20 70,32z" fill="#4dabf7" />}
      </g>
    </svg>
  )
}
