import { useLayoutEffect, useMemo, useRef, useState } from 'react'

// Single-series line chart with a hover crosshair. One measure per chart (small multiples).
export default function LineChart({
  title,
  values,
  labels,
  format = (v) => v.toFixed(1),
  unit = '',
  target = null,
  targetLabel = 'Target',
  upto = values.length,
  height = 150,
  color = 'var(--chart)',
  goodDirection = null, // 'down' | 'up': colours the change pill
  fill = false, // draw at the size of its box (for one-screen layouts) instead of a fixed shape
}) {
  const plotRef = useRef(null)
  const [box, setBox] = useState(null)
  useLayoutEffect(() => {
    if (!fill || !plotRef.current) return
    const observer = new ResizeObserver(([entry]) => {
      const { width, height: h } = entry.contentRect
      if (width > 40 && h > 40) setBox({ w: Math.round(width), h: Math.round(h) })
    })
    observer.observe(plotRef.current)
    return () => observer.disconnect()
  }, [fill])
  const W = box ? box.w : 320
  const H = box ? box.h : height
  const pad = { l: 38, r: 46, t: 12, b: 22 }
  const wrapRef = useRef(null)
  const [hover, setHover] = useState(null)

  const { yMin, yMax, ticks } = useMemo(() => {
    const all = values.concat(target != null ? [target] : [])
    let lo = Math.min(...all), hi = Math.max(...all)
    if (hi - lo < 1) { hi += 0.5; lo -= 0.5 }
    const span = hi - lo
    lo -= span * 0.1
    hi += span * 0.1
    const step = niceStep(span / 3)
    const start = Math.ceil(lo / step) * step
    const t = []
    for (let v = start; v <= hi; v += step) t.push(+v.toFixed(6))
    return { yMin: lo, yMax: hi, ticks: t }
  }, [values, target])

  const x = (i) => pad.l + (i / (values.length - 1)) * (W - pad.l - pad.r)
  const y = (v) => pad.t + (1 - (v - yMin) / (yMax - yMin)) * (H - pad.t - pad.b)
  const shown = values.slice(0, Math.max(1, upto))
  const d = shown.map((v, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ')
  const lastI = shown.length - 1
  const change = shown[lastI] - values[0]
  const changeGood = goodDirection == null ? null : goodDirection === 'down' ? change < 0 : change > 0

  const onMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect()
    // The drawing keeps its shape, so it may sit centred with empty space beside it.
    const scale = Math.min(rect.width / W, rect.height / H)
    const px = (e.clientX - rect.left - (rect.width - W * scale) / 2) / scale
    const i = Math.round(((px - pad.l) / (W - pad.l - pad.r)) * (values.length - 1))
    setHover(Math.max(0, Math.min(lastI, i)))
  }

  return (
    <figure className="chart" ref={wrapRef}>
      <figcaption>
        <span className="chart-title">{title}</span>
        <span className="chart-now">
          {format(shown[lastI])}{unit}
          {lastI > 0 && Math.abs(change) >= 0.05 && (
            <span className={`pill ${changeGood == null ? '' : changeGood ? 'good' : 'bad'}`}>
              {change > 0 ? '▲' : '▼'} {format(Math.abs(change))}
            </span>
          )}
        </span>
      </figcaption>
      <div className={`chart-plot ${fill ? 'fill' : ''}`} ref={plotRef}>
        <svg viewBox={`0 0 ${W} ${H}`} onMouseMove={onMove} onMouseLeave={() => setHover(null)} role="img"
          aria-label={`${title}: from ${format(values[0])}${unit} to ${format(shown[lastI])}${unit}`}>
          {ticks.map((t) => (
            <g key={t}>
              <line x1={pad.l} x2={W - pad.r} y1={y(t)} y2={y(t)} className="grid" />
              <text x={pad.l - 6} y={y(t) + 3.5} textAnchor="end" className="tick">{format(t)}</text>
            </g>
          ))}
          {labels.map((l, i) => (i % 2 === 0 || i === labels.length - 1) && (
            <text key={i} x={x(i)} y={H - 6} textAnchor="middle" className="tick">{l}</text>
          ))}
          {target != null && (
            <g>
              <line x1={pad.l} x2={W - pad.r} y1={y(target)} y2={y(target)} className="target-line" />
              <text x={W - pad.r + 4} y={y(target) + 3.5} className="tick">{targetLabel}</text>
            </g>
          )}
          <path d={d} fill="none" stroke={color} strokeWidth="2.25" strokeLinejoin="round" strokeLinecap="round" />
          <circle cx={x(lastI)} cy={y(shown[lastI])} r="4.5" fill={color} stroke="var(--paper)" strokeWidth="2" />
          {hover != null && (
            <g>
              <line x1={x(hover)} x2={x(hover)} y1={pad.t} y2={H - pad.b} className="crosshair" />
              <circle cx={x(hover)} cy={y(values[hover])} r="4.5" fill={color} stroke="var(--paper)" strokeWidth="2" />
            </g>
          )}
          <rect x={pad.l} y={pad.t} width={W - pad.l - pad.r} height={H - pad.t - pad.b} fill="transparent" />
        </svg>
        {hover != null && (
          <div className="tooltip" style={{ left: `${(x(hover) / W) * 100}%`, top: `${(y(values[hover]) / H) * 100}%` }}>
            <strong>{labels[hover]}</strong>
            <span>{format(values[hover])}{unit}</span>
          </div>
        )}
      </div>
    </figure>
  )
}

function niceStep(raw) {
  const p = Math.pow(10, Math.floor(Math.log10(raw)))
  const n = raw / p
  return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * p
}
