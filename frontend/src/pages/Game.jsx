import { useCallback, useEffect, useRef, useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { api } from '../api'
import { loadPlay, savePlay } from '../play'
import Explain from '../components/Explain'
import Hud from '../components/Hud'
import Modal from '../components/Modal'
import IslandArt from '../components/IslandArt'
import { skyForTime } from '../series'
import Portrait from '../components/Portrait'
import TopBar from '../components/TopBar'
import MobileWarning from '../components/MobileWarning'
import useSceneFit from '../components/useSceneFit'
import WorldMap from '../components/WorldMap'

const DELTA_LABELS = {
  approval: ['Approval', (v) => `${Math.round(v)} pts`, 1],
  currency_index: ['Currency', (v) => v.toFixed(1), 1],
  reserves_months: ['Reserves', (v) => `${v.toFixed(1)} months`, 1],
  debt_to_gdp: ['Debt', (v) => `${v.toFixed(1)}% GDP`, -1],
  interest_rate: ['Interest rate', (v) => `${v.toFixed(1)}%`, 0],
}

function Progress({ step, total, time, onPick }) {
  return (
    <div className="progress">
      <span className="clock" aria-label={`Time ${time}`}>🕰️ {time}</span>
      <span className="dots" aria-label={`Decision ${Math.min(step + 1, total)} of ${total}`}>
        {Array.from({ length: total }, (_, i) => i < step ? (
          <button key={i} className="done" onClick={() => onPick(i)} title={`Look back at decision ${i + 1}`}
            aria-label={`Look back at decision ${i + 1}`} />
        ) : <span key={i} className={i === step ? 'now' : ''} />)}
      </span>
    </div>
  )
}

// The day's visitors in order: what you chose (click to look back), who is in the office now,
// and who is still waiting outside.
function Agenda({ game, onPick }) {
  const crowd = { cheer: ['good', 'Cheered'], boo: ['bad', 'Booed'], mixed: ['', 'Mixed'] }
  return (
    <section className="agenda panel" aria-label="Today's appointments">
      <h3>Today's appointments</h3>
      <ol>
        {game.agenda.map((a, i) => {
          const done = game.decisions[i]
          const now = i === game.step
          const inner = (
            <>
              <span className="agenda-time">{a.time}</span>
              <Portrait kind={a.speaker_icon} size={26} />
              <span className="agenda-what">
                {done ? <><span aria-hidden>{done.icon}</span> {done.option_title}</> : a.speaker}
              </span>
              {done && <span className={`chip ${crowd[done.reaction.crowd][0]}`}>{crowd[done.reaction.crowd][1]}</span>}
              {now && <span className="chip now">In your office</span>}
            </>
          )
          return (
            <li key={i} className={done ? 'done' : now ? 'now' : 'later'}>
              {done ? <button onClick={() => onPick(i)} title="Look back at this decision">{inner}</button> : <div>{inner}</div>}
            </li>
          )
        })}
      </ol>
    </section>
  )
}

function Briefing({ scenario, map }) {
  return (
    <>
      <p className="lede"><Explain>{scenario.intro}</Explain></p>
      <ul className="briefing">
        {scenario.briefing.map((b) => <li key={b}><Explain>{b}</Explain></li>)}
      </ul>
      {map}
    </>
  )
}

function OptionGrid({ card, chosenId, onChoose, disabled }) {
  return (
    <div className={`options n${card.options.length}`}>
      {card.options.map((o, i) => (
        <motion.button
          key={o.id}
          className={`option ${o.id === chosenId ? 'chosen' : ''}`}
          onClick={onChoose ? () => onChoose(o) : undefined}
          disabled={disabled || !onChoose}
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 + i * 0.07 }}
          whileHover={onChoose ? { y: -4 } : undefined}
          whileTap={onChoose ? { scale: 0.97 } : undefined}
        >
          <span className="option-icon" aria-hidden>{o.icon}</span>
          <span className="option-title">{o.title}{o.id === chosenId && <span className="chosen-tag">Your choice</span>}</span>
          <span className="option-summary"><Explain nested>{o.summary}</Explain></span>
        </motion.button>
      ))}
    </div>
  )
}

export default function Game() {
  const navigate = useNavigate()
  const [play, setPlay] = useState(loadPlay)
  const [game, setGame] = useState(null)
  const [world, setWorld] = useState([])
  const [reaction, setReaction] = useState(null) // { option, reaction, nextGame }
  const [introSeen, setIntroSeen] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [showBriefing, setShowBriefing] = useState(false)
  const [review, setReview] = useState(null) // index of a past decision being looked at
  const closeBriefing = useCallback(() => setShowBriefing(false), [])
  const closeReview = useCallback(() => setReview(null), [])
  const sceneCol = useRef(null)
  useSceneFit(sceneCol)

  useEffect(() => {
    if (!play) return
    Promise.all([api.play(play), api.islands()])
      .then(([g, i]) => {
        setGame(g)
        setWorld(i.world)
        setIntroSeen(g.step > 0)
      })
      .catch((e) => setError(e.message))
    // Only on arrival: later choices update `game` directly.
  }, [])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [game?.step, reaction, introSeen])

  if (!play) return <Navigate to="/" replace />
  if (error && !game) return <div className="page"><TopBar /><div className="loading-screen">{error}</div></div>
  if (!game) return <div className="page"><TopBar /><div className="loading-screen">Unlocking your office…</div></div>

  const island = game.island
  const card = game.card
  const chosen = Object.fromEntries(game.decisions.map((d) => [d.card_id, d.option_id]))
  const stance = chosen.war || null
  const scenario = game.scenario
  const map = scenario.map ? <WorldMap island={island} world={world} mode={scenario.map} stance={stance} /> : null
  const time = reaction ? reaction.time : card ? card.time : '21:00'
  const lastCrowd = reaction ? reaction.reaction.crowd : game.decisions.at(-1)?.reaction.crowd || 'mixed'

  const choose = async (option) => {
    if (busy) return
    setBusy(true)
    setError('')
    try {
      const res = await api.decide(play, card.id, option.id)
      setPlay(savePlay({ ...play, decisions: [...play.decisions, [card.id, option.id]] }))
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

  const fastForward = () => navigate('/play/forward')

  // Go back to an earlier visitor and decide again. Everything after it is cleared.
  const rewind = async (step) => {
    const later = play.decisions.length - step - 1
    if (later > 0 && !window.confirm(`Change this decision? Your ${later} later decision${later > 1 ? 's' : ''} will be cleared.`)) return
    const rewound = { ...play, decisions: play.decisions.slice(0, step) }
    setBusy(true)
    try {
      setGame(await api.play(rewound))
      setPlay(savePlay(rewound))
      setReaction(null)
      setReview(null)
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }
  const past = review != null ? shownGame().decisions[review] : null

  function shownGame() {
    return reaction ? reaction.nextGame : game
  }

  return (
    <div className={`page fit game-page sky-${skyForTime(time)}`}>
      <MobileWarning />
      <TopBar actions={introSeen && <button className="btn small" onClick={() => setShowBriefing(true)}>📋 Briefing</button>}>
        <Progress step={shownGame().step} total={game.total_steps} time={time} onPick={setReview} />
      </TopBar>
      {showBriefing && (
        <Modal title={`${scenario.icon} ${scenario.title}`} onClose={closeBriefing} wide>
          <Briefing scenario={scenario} map={map} />
        </Modal>
      )}
      {past && (
        <Modal title={`${past.time} · ${past.card.title}`} onClose={closeReview} wide>
          <div className="visitor">
            <Portrait kind={past.card.speaker_icon} size={56} />
            <span className="eyebrow">{past.card.speaker}</span>
          </div>
          <div className="speech"><Explain>{past.card.situation}</Explain></div>
          <OptionGrid card={past.card} chosenId={past.option_id} />
          <div className="review-foot">
            <span className="muted small">The crowd {past.reaction.crowd === 'cheer' ? 'cheered' : past.reaction.crowd === 'boo' ? 'booed' : 'was unsure'}: {past.reaction.quote}</span>
            <button className="btn" onClick={() => rewind(past.step)} disabled={busy}>↩ Change this decision</button>
          </div>
        </Modal>
      )}
      <Hud stats={shownGame().live_stats} deltas={reaction?.reaction.deltas} currencyCode={island.currency_code} />

      <main className="day-layout">
        <section className="scene-col" ref={sceneCol}>
          <div className="scene-box">
          <div className="scene-frame">
            <IslandArt
              fill
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
          </div>
          {/* The world map lives in the Briefing; this spot shows the day's appointments. */}
          <Agenda game={shownGame()} onPick={setReview} />
        </section>

        <section className="desk-col">
          <AnimatePresence mode="wait">
            {!introSeen && card && (
              <motion.div key="intro" className="panel desk intro" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
                <span className="eyebrow">Day 1 · {scenario.category} · {scenario.title}</span>
                <h1>Good morning, Governor.</h1>
                <Briefing scenario={scenario} map={null} />
                <p>
                  {game.total_steps} people will come to your office today. Each one brings a problem, and each choice
                  gets an instant reaction. The real consequences show up later, when we fast-forward two years.
                </p>
                {map}
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
                <div className="speech"><Explain>{card.situation}</Explain></div>
                <OptionGrid card={card} onChoose={choose} disabled={busy} />
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
