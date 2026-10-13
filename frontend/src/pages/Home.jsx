import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api'
import { useAuth } from '../auth'
import IslandArt from '../components/IslandArt'
import TopBar from '../components/TopBar'
import MobileWarning from '../components/MobileWarning'

export default function Home() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [games, setGames] = useState(null)
  const [islands, setIslands] = useState({})
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([api.games(), api.islands()])
      .then(([g, i]) => {
        setGames(g)
        setIslands(Object.fromEntries(i.islands.map((x) => [x.id, x])))
      })
      .catch((e) => setError(e.message))
  }, [])

  const remove = async (id) => {
    if (!window.confirm('Delete this term and all its decisions?')) return
    await api.deleteGame(id)
    setGames((gs) => gs.filter((g) => g.id !== id))
  }

  return (
    <div className="page">
      <MobileWarning />
      <TopBar />
      <main className="home">
        <section className="home-hero">
          <div>
            <h1>Welcome, Governor {user.username}</h1>
            <p className="lede">
              Every term you serve is saved here. You can resume a day you didn't finish or look back at the report
              from one you did.
            </p>
            <button className="btn primary big" onClick={() => navigate('/new')}>Take office on a new island →</button>
          </div>
        </section>

        {error && <p className="error">{error}</p>}
        {games && games.length === 0 && (
          <div className="empty panel">
            <p>You haven't served a term yet. Pick an island and see how your first day goes.</p>
          </div>
        )}
        {games && games.length > 0 && (
          <section>
            <h2>Your terms in office</h2>
            <div className="term-grid">
              {games.map((g, i) => {
                const island = islands[g.island_id]
                const done = g.status === 'completed'
                return (
                  <motion.article key={g.id} className="panel term-card" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
                    {island && <IslandArt island={island} crowd={false} boats={1} className="term-art" />}
                    <div className="term-body">
                      <div className="term-head">
                        <h3>{g.island_name}</h3>
                        <span className={`tier tier-${island?.tier}`}>{g.tier_label}</span>
                      </div>
                      <p className="term-crisis"><span aria-hidden>{g.scenario_icon}</span> {g.scenario_title}</p>
                      {done ? (
                        <p className="term-status"><strong>{g.ending}</strong> · Score {g.score}</p>
                      ) : (
                        <p className="term-status">In office: decision {Math.min(g.step + 1, g.total_steps)} of {g.total_steps}</p>
                      )}
                      <p className="muted small">{new Date(g.updated_at).toLocaleString()}</p>
                      <div className="term-actions">
                        {done ? (
                          <Link className="btn" to={`/game/${g.id}/report`}>View report</Link>
                        ) : (
                          <Link className="btn primary" to={`/game/${g.id}`}>Resume</Link>
                        )}
                        <button className="btn ghost" onClick={() => remove(g.id)} aria-label={`Delete term on ${g.island_name}`}>Delete</button>
                      </div>
                    </div>
                  </motion.article>
                )
              })}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}
