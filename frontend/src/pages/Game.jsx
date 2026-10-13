import { useEffect, useState } from 'react'
import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { api } from '../api'
import Hud from '../components/Hud'
import IslandArt from '../components/IslandArt'
import { skyForTime } from '../series'
import Portrait from '../components/Portrait'
import TopBar from '../components/TopBar'
import WorldMap from '../components/WorldMap'

const DELTA_LABELS = {
  approval: ['Approval', (v) => `${Math.round(v)} pts`, 1],
  currency_index: ['Currency', (v) => v.toFixed(1), 1],
  reserves_months: ['Reserves', (v) => `${v.toFixed(1)} months`, 1],
  debt_to_gdp: ['Debt', (v) => `${v.toFixed(1)}% GDP`, -1],
  interest_rate: ['Interest rate', (v) => `${v.toFixed(1)}%`, 0],
}

function Progress({ step, total, time }) {
  return (
    <div className="progress">
      <span className="clock" aria-label={`Time ${time}`}>🕰️ {time}</span>
      <span className="dots" aria-label={`Decision ${Math.min(step + 1, total)} of ${total}`}>
        {Array.from({ length: total }, (_, i) => <span key={i} className={i < step ? 'done' : i === step ? 'now' : ''} />)}
      </span>
    </div>
  )
}

export default function Game() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [game, setGame] = useState(null)
  const [world, setWorld] = useState([])
  const [reaction, setReaction] = useState(null) // { option, reaction, nextGame }
  const [introSeen, setIntroSeen] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([api.game(id), api.islands()])
      .then(([g, i]) => {
        setGame(g)
        setWorld(i.world)
        setIntroSeen(g.step > 0)
      })
      .catch((e) => setError(e.message))
  }, [id])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [game?.step, reaction, introSeen])

  if (error && !game) return <div className="page"><TopBar /><div className="loading-screen">{error}</div></div>
  if (!game) return <div className="page"><TopBar /><div className="loading-screen">Unlocking your office…</div></div>
  if (game.status === 'completed') return <Navigate to={`/game/${id}/report`} replace />

  const island = game.island
  const card = game.card
  const chosen = Object.fromEntries(game.decisions.map((d) => [d.card_id, d.option_id]))
  const stance = chosen.war || null
  const time = reaction ? reaction.time : card ? card.time : '21:00'
  const lastCrowd = reaction ? reaction.reaction.crowd : game.decisions.at(-1)?.reaction.crowd || 'mixed'

  const choose = async (option) => {
    if (busy) return
    setBusy(true)
    setError('')
    try {
      const res = await api.decide(game.id, card.id, option.id)
      setReaction({ option, reaction: res.reaction, nextGame: res.game, time: card.time, speaker: card.speaker_icon })
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  const next = () => {
    setGame(reaction.nextGame)
    setReaction(null)
  }

  const fastForward = async () => {
    setBusy(true)
    try {
      await api.fastForward(game.id)
      navigate(`/game/${game.id}/forward`)
    } catch (e) {
      setError(e.message)
      setBusy(false)
    }
  }

  const shownGame = reaction ? reaction.nextGame : game

  return (
    <div className={`page game-page sky-${skyForTime(time)}`}>
      <TopBar>
        <Progress step={shownGame.step} total={game.total_steps} time={time} />
      </TopBar>
      <Hud stats={shownGame.live_stats} deltas={reaction?.reaction.deltas} currencyCode={island.currency_code} />

      <main className="day-layout">
        <section className="scene-col">
          <div className="scene-frame">
            <IslandArt
              island={island}
              sky={skyForTime(time)}
              mood={lastCrowd}
              green={chosen.future === 'green'}
              smoke={0.7}
              boats={stance === 'neutral' ? 3 : 2}
            />
            <AnimatePresence>
              {reaction && (
                <motion.div className="speech crowd-speech" initial={{ opacity: 0, scale: 0.8, y: 10 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0 }}>
                  {reaction.reaction.quote}
                </motion.div>
              )}
            </AnimatePresence>
            <div className="scene-caption">
              <strong>{island.name}</strong> · {island.tier_label}
            </div>
          </div>
          {introSeen && (
            <div className="mini-map">
              <WorldMap island={island} world={world} atWar stance={stance} compact />
            </div>
          )}
        </section>

        <section className="desk-col">
          <AnimatePresence mode="wait">
            {!introSeen && card && (
              <motion.div key="intro" className="panel desk intro" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
                <span className="eyebrow">Day 1 · {game.scenario.title}</span>
                <h1>Good morning, Governor.</h1>
                <p className="lede">{game.scenario.intro}</p>
                <p>
                  Seven people will come to your office today. Each one brings a problem, and each choice gets an
                  instant reaction. The real consequences show up later, when we fast-forward two years.
                </p>
                <WorldMap island={island} world={world} atWar />
                <button className="btn primary big" onClick={() => setIntroSeen(true)}>Open the office doors</button>
              </motion.div>
            )}

            {introSeen && card && !reaction && (
              <motion.div key={card.id} className="panel desk" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
                <div className="visitor">
                  <Portrait kind={card.speaker_icon} size={76} />
                  <div>
                    <span className="eyebrow">{card.time} · {card.speaker}</span>
                    <h2>{card.title}</h2>
                  </div>
                </div>
                <div className="speech">{card.situation}</div>
                <div className={`options n${card.options.length}`}>
                  {card.options.map((o, i) => (
                    <motion.button
                      key={o.id}
                      className="option"
                      onClick={() => choose(o)}
                      disabled={busy}
                      initial={{ opacity: 0, y: 14 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.15 + i * 0.07 }}
                      whileHover={{ y: -4 }}
                      whileTap={{ scale: 0.97 }}
                    >
                      <span className="option-icon" aria-hidden>{o.icon}</span>
                      <span className="option-title">{o.title}</span>
                      <span className="option-summary">{o.summary}</span>
                    </motion.button>
                  ))}
                </div>
                {error && <p className="error">{error}</p>}
              </motion.div>
            )}

            {reaction && (
              <motion.div key="reaction" className="panel desk reaction" initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}>
                <span className="eyebrow">Decision signed</span>
                <h2><span aria-hidden>{reaction.option.icon}</span> {reaction.option.title}</h2>
                <div className={`crowd-verdict ${reaction.reaction.crowd}`}>
                  {reaction.reaction.crowd === 'cheer' ? '📣 The crowd outside cheers!' : reaction.reaction.crowd === 'boo' ? '😠 Boos from the square outside.' : '🤔 The crowd murmurs, unsure.'}
                </div>
                <h3>What happened straight away</h3>
                <ul className="delta-list">
                  {Object.entries(DELTA_LABELS).map(([k, [label, fmt, better]]) => {
                    const v = reaction.reaction.deltas[k]
                    if (v == null || Math.abs(v) < 0.05) return null
                    const tone = better === 0 ? '' : v * better > 0 ? 'good' : 'bad'
                    return (
                      <li key={k} className={tone}>
                        <span>{label}</span>
                        <strong>{v > 0 ? '▲ +' : '▼ −'}{fmt(Math.abs(v))}</strong>
                      </li>
                    )
                  })}
                  {Object.values(reaction.reaction.deltas).every((v) => Math.abs(v) < 0.05) && <li><span>Nothing visible yet</span></li>}
                </ul>
                <p className="foreshadow">⏳ The deeper effects (on prices, jobs and savings) take months to show up. You'll see them when time fast-forwards.</p>
                <button className="btn primary big" onClick={next} autoFocus>
                  {reaction.nextGame.card ? `Next visitor (${reaction.nextGame.card.time}) →` : 'End the day →'}
                </button>
              </motion.div>
            )}

            {!card && !reaction && (
              <motion.div key="dayover" className="panel desk dayover" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                <span className="eyebrow">21:00 · The office lights go out</span>
                <h1>Your day is done.</h1>
                <p className="lede">You made {game.decisions.length} decisions. Here's what you signed:</p>
                <ol className="signed">
                  {game.decisions.map((d) => {
                    const r = d.reaction
                    return (
                      <li key={d.step}>
                        <span className={`chip ${r.crowd}`}>{r.crowd === 'cheer' ? 'Cheered' : r.crowd === 'boo' ? 'Booed' : 'Mixed'}</span>
                        <span className="signed-time">{d.time}</span>
                        <span><span aria-hidden>{d.icon}</span> <strong>{d.option_title}</strong> <span className="muted">· {d.card_title}</span></span>
                      </li>
                    )
                  })}
                </ol>
                <p>Approval tonight: <strong>{Math.round(game.live_stats.approval)}%</strong>. Now let's see how history judges you.</p>
                {error && <p className="error">{error}</p>}
                <button className="btn primary big" onClick={fastForward} disabled={busy}>
                  {busy ? 'Running the simulation…' : '⏩ Fast-forward two years'}
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </section>
      </main>
    </div>
  )
}
