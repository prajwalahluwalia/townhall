import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { api } from '../api'
import IslandArt from '../components/IslandArt'
import TopBar from '../components/TopBar'

const DIFFICULTY = { rich: 1, developed: 2, developing: 3, poor: 4, very_poor: 5 }

function Bar({ label, value, note }) {
  return (
    <div className="bar-row">
      <span className="bar-label">{label}</span>
      <span className="bar-track"><motion.span className="bar-fill" initial={{ width: 0 }} animate={{ width: `${Math.max(4, value * 100)}%` }} /></span>
      <span className="bar-note">{note}</span>
    </div>
  )
}

export default function IslandSelect() {
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [picked, setPicked] = useState('coralia')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api.islands().then(setData).catch((e) => setError(e.message))
  }, [])

  const start = async () => {
    setBusy(true)
    try {
      const game = await api.newGame(picked)
      navigate(`/game/${game.id}`)
    } catch (e) {
      setError(e.message)
      setBusy(false)
    }
  }

  if (!data) return <div className="page"><TopBar /><div className="loading-screen">{error || 'Charting the seas…'}</div></div>
  const island = data.islands.find((i) => i.id === picked)
  const s = island.start

  return (
    <div className="page">
      <TopBar />
      <main className="select">
        <div className="select-head">
          <h1>Choose your island</h1>
          <p className="lede">
            All five islands face the same war tomorrow morning. How it plays out depends on how rich each one is, how
            much people trust its money, and how much it depends on fuel and food from abroad.
          </p>
        </div>

        <div className="select-layout">
          <div className="archipelago" role="radiogroup" aria-label="Islands">
            {data.islands.map((i, idx) => (
              <motion.button
                key={i.id}
                role="radio"
                aria-checked={picked === i.id}
                className={`isle isle-${idx} ${picked === i.id ? 'picked' : ''}`}
                onClick={() => setPicked(i.id)}
                whileHover={{ y: -4 }}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.06 }}
              >
                <IslandArt island={i} crowd={false} boats={i.tier === 'rich' ? 3 : i.tier === 'very_poor' ? 1 : 2} smoke={0.6} />
                <span className="isle-name">{i.name}</span>
                <span className={`tier tier-${i.tier}`}>{i.tier_label}</span>
              </motion.button>
            ))}
          </div>

          <AnimatePresence mode="wait">
            <motion.aside key={island.id} className="panel island-detail" initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}>
              <div className="detail-head">
                <h2>{island.name}</h2>
                <span className={`tier tier-${island.tier}`}>{island.tier_label}</span>
              </div>
              <p className="tagline">{island.tagline}</p>
              <p>{island.description}</p>

              <dl className="facts">
                <div><dt>Population</dt><dd>{island.population}</dd></div>
                <div><dt>Income per person</dt><dd>${island.gdp_per_capita.toLocaleString()}</dd></div>
                <div><dt>Currency</dt><dd>{island.currency}</dd></div>
                <div><dt>Inflation today</dt><dd>{s.inflation}%</dd></div>
                <div><dt>Unemployment</dt><dd>{s.unemployment}%</dd></div>
                <div><dt>Interest rate</dt><dd>{s.interest_rate}%</dd></div>
              </dl>

              <div className="bars">
                <Bar label="Trust in its money" value={island.credibility} note={island.credibility > 0.7 ? 'High' : island.credibility > 0.45 ? 'Shaky' : 'Low'} />
                <Bar label="Savings (reserves)" value={Math.min(1, s.reserves_months / 14)} note={`${s.reserves_months} months`} />
                <Bar label="Energy independence" value={1 - island.fuel_dependence} note={`${Math.round(island.fuel_dependence * 100)}% imported`} />
                <Bar label="Debt burden" value={Math.min(1, s.debt_to_gdp / 120)} note={`${s.debt_to_gdp}% of GDP`} />
                <Bar label="Sustainability" value={s.sustainability / 100} note={`${Math.round(s.sustainability)}/100`} />
              </div>

              <div className="company-box">
                <span className="eyebrow">Biggest employer</span>
                <strong>{island.company.name}</strong>
                <span className="muted small">{island.company.workers} workers · {island.company.sector}</span>
              </div>

              {island.un_eligible && <p className="un-note">🇺🇳 This island can ask the UN and IMF for an emergency package.</p>}
              {error && <p className="error">{error}</p>}

              <div className="detail-foot">
                <div className="difficulty" aria-label={`Difficulty ${DIFFICULTY[island.tier]} of 5`}>
                  <span className="difficulty-label">Difficulty</span>
                  {'●'.repeat(DIFFICULTY[island.tier])}<span className="dim">{'●'.repeat(5 - DIFFICULTY[island.tier])}</span>
                </div>
                <button className="btn primary big" onClick={start} disabled={busy}>
                  {busy ? 'Swearing you in…' : `Become Governor of ${island.name}`}
                </button>
              </div>
            </motion.aside>
          </AnimatePresence>
        </div>
      </main>
    </div>
  )
}
