import { useEffect, useRef, useState } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { api } from '../api'
import { CAUSE_COLORS, CAUSES } from '../causes'
import Explain from '../components/Explain'
import { loadPlay } from '../play'
import IslandArt from '../components/IslandArt'
import LineChart from '../components/LineChart'
import Portrait from '../components/Portrait'
import TopBar from '../components/TopBar'
import useSceneFit from '../components/useSceneFit'
import { moodFromApproval, seriesOf, quarterLabels } from '../series'

const STEP_MS = 3400

// What made up inflation this quarter: the causes pushing prices up as one stacked bar,
// and anything pulling them down listed underneath.
function InflationMix({ quarter, labels }) {
  if (!quarter) {
    return (
      <section className="mix panel">
        <h3>What is pushing prices?</h3>
        <p className="muted">Each quarter, this splits inflation into its causes.</p>
      </section>
    )
  }
  const parts = Object.entries(quarter.inflation_causes).filter(([, v]) => Math.abs(v) >= 0.1)
  const up = parts.filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1])
  const down = parts.filter(([, v]) => v < 0).sort((a, b) => a[1] - b[1])
  const total = up.reduce((t, [, v]) => t + v, 0)
  return (
    <section className="mix panel">
      <h3><Explain>{`What made up ${quarter.inflation.toFixed(1)}% inflation`}</Explain></h3>
      <div className="mix-bar" role="img" aria-label={up.map(([k, v]) => `${labels[k][0]} ${v.toFixed(1)} points`).join(', ')}>
        {up.map(([k, v]) => (
          <motion.span key={k} title={`${labels[k][0]}: +${v.toFixed(1)}`} style={{ background: CAUSE_COLORS[k] }}
            initial={false} animate={{ width: `${(v / total) * 100}%` }} transition={{ duration: 0.6 }} />
        ))}
      </div>
      <ul className="mix-legend">
        {up.map(([k, v]) => (
          <li key={k}><i style={{ background: CAUSE_COLORS[k] }} />{labels[k][0]} <strong>+{v.toFixed(1)}</strong></li>
        ))}
        {down.map(([k, v]) => (
          <li key={k} className="down"><i style={{ background: CAUSE_COLORS[k] }} />{labels[k][0]} <strong>−{Math.abs(v).toFixed(1)}</strong></li>
        ))}
      </ul>
    </section>
  )
}

export default function FastForward() {
  const [play] = useState(loadPlay)
  const sceneCol = useRef(null)
  useSceneFit(sceneCol)
  const [report, setReport] = useState(null)
  const [q, setQ] = useState(0) // 0..8, number of quarters revealed
  const [playing, setPlaying] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (play) api.report(play).then(setReport).catch((e) => setError(e.message))
  }, [play])

  useEffect(() => {
    if (!report || !playing) return
    if (q >= report.simulation.timeline.length) return
    const t = setTimeout(() => setQ((x) => x + 1), q === 0 ? 1200 : STEP_MS)
    return () => clearTimeout(t)
  }, [report, q, playing])

  if (!play) return <Navigate to="/" replace />
  if (!report) return <div className="page"><TopBar /><div className="loading-screen">{error || 'Turning the pages of the calendar…'}</div></div>

  const sim = report.simulation
  const tl = sim.timeline
  const done = q >= tl.length
  const current = q > 0 ? tl[q - 1] : null
  const labels = quarterLabels(tl.length)
  const chosenGreen = report.consequence_map.some((c) => c.option_id === 'green')
  const news = q > 0 ? report.headlines[q - 1] : null
  const approval = current ? current.approval : sim.start.approval_after_day

  return (
    <div className="page fit forward-page">
      <TopBar>
        <div className="progress">
          <span className="clock">⏩ {current ? `${current.months} months later` : 'The next morning'}</span>
          <span className="dots">{tl.map((_, i) => <span key={i} className={i < q ? 'done' : ''} />)}</span>
        </div>
      </TopBar>

      <main className="forward-layout">
        <section className="forward-scene" ref={sceneCol}>
          <div className="scene-box">
          <div className="scene-frame">
            <IslandArt fill island={report.island} sky="noon"
              mood={moodFromApproval(approval)}
              smoke={current ? Math.max(0, Math.min(1, 0.5 + current.output_gap / 6)) : 0.6}
              green={chosenGreen && current && current.quarter >= 5}
              boats={current?.active ? 1 : 3}
            />
            <div className="scene-caption">
              <strong>{report.island.name}</strong> · {current ? (current.active ? report.scenario.status.active : report.scenario.status.over) : 'Day 2'}
            </div>
          </div>
          </div>

          <AnimatePresence mode="wait">
            <motion.article key={q} className="newspaper" initial={{ rotate: -2, opacity: 0, y: 20 }} animate={{ rotate: 0, opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
              <header>
                <span className="paper-name">The {report.island.name} Times</span>
                <span className="paper-date">{current ? `Quarter ${current.quarter} · Month ${current.months}` : 'Special edition'}</span>
              </header>
              {news ? (
                <>
                  <h2 className={news.items[0].tone}>{news.items[0].text}</h2>
                  {news.items.slice(1).map((it, i) => <p key={i} className={`sub ${it.tone}`}>{it.text}</p>)}
                </>
              ) : (
                <h2>Governor's first day ends. Island waits to see what it will cost.</h2>
              )}
            </motion.article>
          </AnimatePresence>

          <div className="citizens-row" aria-label="How people are doing">
            {report.citizens.map((c) => {
              const mood = current ? current.citizens[c.id] : 55
              return (
                <div key={c.id} className="citizen-mini" title={`${c.name}: ${c.role}`}>
                  <Portrait kind={c.avatar} size={52} mood={mood} label={c.name} />
                  <span>{c.name}</span>
                  <span className="mood-bar"><span style={{ width: `${mood}%` }} className={mood < 38 ? 'low' : mood >= 62 ? 'high' : ''} /></span>
                </div>
              )
            })}
          </div>
        </section>

        <section className="forward-side">
        <div className="forward-charts">
          <LineChart fill title="Inflation" values={seriesOf(sim, 'inflation')} labels={labels} upto={q + 1} unit="%" target={sim.target_inflation} goodDirection="down" />
          <LineChart fill title="Unemployment" values={seriesOf(sim, 'unemployment')} labels={labels} upto={q + 1} unit="%" goodDirection="down" />
          <LineChart fill title={`${report.island.currency} value`} values={seriesOf(sim, 'currency_index')} labels={labels} upto={q + 1} format={(v) => v.toFixed(0)} goodDirection="up" />
          <LineChart fill title="Your approval" values={seriesOf(sim, 'approval')} labels={labels} upto={q + 1} unit="%" format={(v) => v.toFixed(0)} goodDirection="up" />
        </div>
        <InflationMix quarter={current} labels={{ ...CAUSES, ...report.scenario.causes }} />

          <div className="forward-controls">
            {!done && (
              <button className="btn" onClick={() => setPlaying((p) => !p)}>{playing ? '⏸ Pause' : '▶ Play'}</button>
            )}
            {!done && <button className="btn" onClick={() => setQ((x) => Math.min(tl.length, x + 1))}>Next quarter →</button>}
            {done ? (
              <Link className="btn primary big" to="/play/report">See what your decisions caused →</Link>
            ) : (
              <Link className="btn ghost" to="/play/report">Skip to report</Link>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}
