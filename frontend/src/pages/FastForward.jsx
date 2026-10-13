import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { api } from '../api'
import IslandArt from '../components/IslandArt'
import LineChart from '../components/LineChart'
import Portrait from '../components/Portrait'
import TopBar from '../components/TopBar'
import { moodFromApproval, seriesOf, quarterLabels } from '../series'

const STEP_MS = 3400

export default function FastForward() {
  const { id } = useParams()
  const [report, setReport] = useState(null)
  const [q, setQ] = useState(0) // 0..8, number of quarters revealed
  const [playing, setPlaying] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.report(id).then(setReport).catch((e) => setError(e.message))
  }, [id])

  useEffect(() => {
    if (!report || !playing) return
    if (q >= report.simulation.timeline.length) return
    const t = setTimeout(() => setQ((x) => x + 1), q === 0 ? 1200 : STEP_MS)
    return () => clearTimeout(t)
  }, [report, q, playing])

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
    <div className="page forward-page">
      <TopBar>
        <div className="progress">
          <span className="clock">⏩ {current ? `${current.months} months later` : 'The next morning'}</span>
          <span className="dots">{tl.map((_, i) => <span key={i} className={i < q ? 'done' : ''} />)}</span>
        </div>
      </TopBar>

      <main className="forward-layout">
        <section className="forward-scene">
          <div className="scene-frame">
            <IslandArt island={report.island} sky="noon"
              mood={moodFromApproval(approval)}
              smoke={current ? Math.max(0, Math.min(1, 0.5 + current.output_gap / 6)) : 0.6}
              green={chosenGreen && current && current.quarter >= 5}
              boats={current?.at_war ? 1 : 3}
            />
            <div className="scene-caption">
              <strong>{report.island.name}</strong> · {current ? (current.at_war ? '⚔️ War continues' : '🕊️ Peace') : 'Day 2'}
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

        <section className="forward-charts">
          <LineChart title="Inflation" values={seriesOf(sim, 'inflation')} labels={labels} upto={q + 1} unit="%" target={sim.target_inflation} goodDirection="down" />
          <LineChart title="Unemployment" values={seriesOf(sim, 'unemployment')} labels={labels} upto={q + 1} unit="%" goodDirection="down" />
          <LineChart title={`${report.island.currency} value`} values={seriesOf(sim, 'currency_index')} labels={labels} upto={q + 1} format={(v) => v.toFixed(0)} goodDirection="up" />
          <LineChart title="Your approval" values={seriesOf(sim, 'approval')} labels={labels} upto={q + 1} unit="%" format={(v) => v.toFixed(0)} goodDirection="up" />

          <div className="forward-controls">
            {!done && (
              <button className="btn" onClick={() => setPlaying((p) => !p)}>{playing ? '⏸ Pause' : '▶ Play'}</button>
            )}
            {!done && <button className="btn" onClick={() => setQ((x) => Math.min(tl.length, x + 1))}>Next quarter →</button>}
            {done ? (
              <Link className="btn primary big" to={`/game/${id}/report`}>See what your decisions caused →</Link>
            ) : (
              <Link className="btn ghost" to={`/game/${id}/report`}>Skip to report</Link>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}
