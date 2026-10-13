import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { api } from '../api'
import { newPlay } from '../play'
import Explain from '../components/Explain'
import IslandArt from '../components/IslandArt'
import TopBar from '../components/TopBar'

const DIFFICULTY = { rich: 1, developed: 2, developing: 3, poor: 4, very_poor: 5 }

function Bar({ label, value, note }) {
  return (
    <div className="bar-row">
      <span className="bar-label"><Explain>{label}</Explain></span>
      <span className="bar-track"><motion.span className="bar-fill" initial={{ width: 0 }} animate={{ width: `${Math.max(4, value * 100)}%` }} /></span>
      <span className="bar-note">{note}</span>
    </div>
  )
}

function ScenarioPicker({ data, island, onBack }) {
  const navigate = useNavigate()
  const [picked, setPicked] = useState(data.scenarios[0].id)
  const scenario = data.scenarios.find((x) => x.id === picked)

  const start = () => {
    newPlay(island.id, scenario.id)
    navigate('/play')
  }

  const surprise = () => {
    const others = data.scenarios.filter((x) => x.id !== picked)
    setPicked(others[Math.floor(Math.random() * others.length)].id)
  }

  return (
    <main className="select">
      <div className="select-head">
        <div>
          <button className="link-back" onClick={onBack}>← Change island</button>
          <h1>What hits {island.name}?</h1>
        </div>
        <p className="lede">
          No government gets to choose its crisis, but you do. Each one hits the economy in a different way and
          brings different people to your office.
        </p>
        <button className="btn surprise" onClick={surprise}>🎲 Surprise me</button>
      </div>

      <div className="select-layout">
        <div className="crisis-grid" role="radiogroup" aria-label="Crises">
          {data.scenarios.map((x, idx) => (
            <motion.button
              key={x.id}
              role="radio"
              aria-checked={picked === x.id}
              className={`crisis-card ${picked === x.id ? 'picked' : ''}`}
              onClick={() => setPicked(x.id)}
              whileHover={{ y: -3 }}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
            >
              <span className="crisis-icon" aria-hidden>{x.icon}</span>
              <span className="crisis-category">{x.category}</span>
              <span className="crisis-title">{x.title}</span>
              <span className="crisis-tagline">{x.tagline}</span>
            </motion.button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          <motion.aside key={scenario.id} className="panel island-detail crisis-detail" initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}>
            <div className="detail-head">
              <h2><span aria-hidden>{scenario.icon}</span> {scenario.title}</h2>
              <span className="tier crisis-chip">{scenario.category}</span>
            </div>
            <p className="tagline">{scenario.tagline}</p>
            <p className="crisis-intro"><Explain>{scenario.intro.replaceAll('your island', island.name)}</Explain></p>

            <h3 className="detail-sub">What hits you on day one</h3>
            <ul className="briefing">
              {scenario.briefing.map((b) => <li key={b}><Explain>{b}</Explain></li>)}
            </ul>

            <div className="company-box">
              <span className="eyebrow">What this crisis teaches</span>
              <span><Explain>{scenario.teaches}</Explain></span>
            </div>

            <div className="governing">
              <IslandArt island={island} crowd={false} boats={1} className="governing-art" />
              <span>You govern <strong>{island.name}</strong> <span className={`tier tier-${island.tier}`}>{island.tier_label}</span></span>
            </div>

            <div className="detail-foot">
              <button className="btn primary big" onClick={start}>Take office: {scenario.title}</button>
            </div>
          </motion.aside>
        </AnimatePresence>
      </div>
    </main>
  )
}

export default function IslandSelect() {
  const [params, setParams] = useSearchParams()
  const [data, setData] = useState(null)
  const [picked, setPicked] = useState(params.get('island') || 'coralia')
  const [error, setError] = useState('')
  const stage = params.get('island') ? 'crisis' : 'island'

  useEffect(() => {
    api.islands().then(setData).catch((e) => setError(e.message))
  }, [])

  useEffect(() => {
    window.scrollTo({ top: 0 })
  }, [stage])

  if (!data) return <div className="page"><TopBar /><div className="loading-screen">{error || 'Charting the seas…'}</div></div>
  const island = data.islands.find((i) => i.id === picked) || data.islands[0]
  const s = island.start

  if (stage === 'crisis') {
    return (
      <div className="page fit">
        <TopBar />
        <ScenarioPicker data={data} island={island} onBack={() => setParams({})} />
      </div>
    )
  }

  return (
    <div className="page fit">
      <TopBar />
      <main className="select">
        <div className="select-head">
          <h1>Choose your island</h1>
          <p className="lede">
            Next you'll pick the crisis that hits it. How it plays out depends on how rich your island is, how much
            people trust its money, and how much it depends on the rest of the world.
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
              <p className="detail-desc"><Explain>{island.description}</Explain></p>

              <dl className="facts">
                <div><dt>Population</dt><dd>{island.population}</dd></div>
                <div><dt><Explain>Income per person</Explain></dt><dd>{island.gdp_per_capita.toLocaleString()} ducats</dd></div>
                <div><dt>Currency</dt><dd>{island.currency}</dd></div>
                <div><dt><Explain>Inflation today</Explain></dt><dd>{s.inflation}%</dd></div>
                <div><dt><Explain>Unemployment</Explain></dt><dd>{s.unemployment}%</dd></div>
                <div><dt><Explain>Interest rate</Explain></dt><dd>{s.interest_rate}%</dd></div>
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

              {island.un_eligible && <p className="un-note">🇺🇳 <Explain>Can ask the UN and IMF for an emergency package.</Explain></p>}
              <div className="detail-foot">
                <div className="difficulty" aria-label={`Difficulty ${DIFFICULTY[island.tier]} of 5`}>
                  <span className="difficulty-label">Difficulty</span>
                  {'●'.repeat(DIFFICULTY[island.tier])}<span className="dim">{'●'.repeat(5 - DIFFICULTY[island.tier])}</span>
                </div>
                <button className="btn primary big" onClick={() => setParams({ island: island.id })}>
                  Govern {island.name}: choose the crisis →
                </button>
              </div>
            </motion.aside>
          </AnimatePresence>
        </div>
      </main>
    </div>
  )
}
