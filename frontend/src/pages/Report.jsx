import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api'
import IslandArt from '../components/IslandArt'
import LineChart from '../components/LineChart'
import Portrait from '../components/Portrait'
import TopBar from '../components/TopBar'
import { moodFromApproval, quarterLabels, seriesOf } from '../series'

const CAUSES = {
  expectations: ['What people already expected', 'Inflation feeds on itself: if everyone expects prices to rise, shops and workers build that in.'],
  fuel: ['Fuel prices (the war)', 'Oil from the strait got scarce and expensive. That cost travels into transport, farming and factories.'],
  food: ['Food prices (the war)', 'Granara\'s grain fields became a battlefield.'],
  printing: ['Newly printed money', 'More money but the same amount of goods, so each unit of money buys less.'],
  currency: ['A weaker currency', 'When your money is worth less abroad, everything you import costs more.'],
  wages: ['Wage rises passed on', 'Higher pay means higher costs, which businesses pass on as higher prices.'],
  demand: ['Spending vs. supply', 'Positive means people were spending more than the island could produce. Negative means a slump pulled prices down.'],
}

const TILES = [
  { key: 'peak_inflation', label: 'Peak inflation', start: (s) => s.inflation, fmt: (v) => `${v.toFixed(1)}%`, better: -1 },
  { key: 'avg_unemployment', label: 'Avg. unemployment', start: (s) => s.unemployment, fmt: (v) => `${v.toFixed(1)}%`, better: -1 },
  { key: 'currency_end', label: 'Currency value', start: (s) => s.currency_index, fmt: (v) => v.toFixed(0), better: 1 },
  { key: 'debt_end', label: 'Government debt', start: (s) => s.debt_to_gdp, fmt: (v) => `${v.toFixed(0)}%`, better: -1 },
  { key: 'reserves_end', label: 'Reserves', start: (s) => s.reserves_months, fmt: (v) => `${v.toFixed(1)} mo`, better: 1 },
  { key: 'sustainability_end', label: 'Sustainability', start: (s) => s.sustainability, fmt: (v) => v.toFixed(0), better: 1 },
]

function ImpactChips({ items }) {
  if (!items?.length) return <p className="muted small">No measurable difference.</p>
  return (
    <ul className="impact-chips">
      {items.map((i) => (
        <li key={i.key} className={i.good ? 'good' : 'bad'}>
          <span aria-hidden>{i.good ? '✓' : '✗'}</span> {i.label} {i.delta > 0 ? '+' : '−'}{Math.abs(i.delta)} {i.unit}
        </li>
      ))}
    </ul>
  )
}

export default function Report() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.report(id).then(setReport).catch((e) => setError(e.message))
  }, [id])

  if (!report) return <div className="page"><TopBar /><div className="loading-screen">{error || 'Writing the history books…'}</div></div>

  const sim = report.simulation
  const tl = sim.timeline
  const last = tl[tl.length - 1]
  const start = sim.start
  const labels = quarterLabels(tl.length)
  const sum = report.summary
  const tileValues = {
    ...sum,
    currency_end: last.currency_index,
    debt_end: last.debt_to_gdp,
  }
  const causes = Object.entries(report.peak.causes).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
  const maxCause = Math.max(...causes.map(([, v]) => Math.abs(v)))
  const chosenGreen = report.consequence_map.some((c) => c.option_id === 'green')
  const currencySym = report.island.currency_code
  const moneyGrowth = ((last.money.bank + last.money.central) / 100 - 1) * 100

  const playAgain = async () => {
    const g = await api.newGame(report.island.id)
    navigate(`/game/${g.id}`)
  }

  return (
    <div className="page report-page">
      <TopBar />
      <main className="report">
        <section className="report-hero panel">
          <div className="hero-text">
            <span className="eyebrow">{report.island.name} · two years after your day in office</span>
            <motion.h1 initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>{report.ending.title}</motion.h1>
            <p className="lede">{report.ending.text}</p>
            <div className="score">
              <motion.span className="score-num" initial={{ scale: 0.6, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.2, type: 'spring' }}>
                {report.score}
              </motion.span>
              <span className="muted">out of 1000</span>
            </div>
            <div className="hero-actions">
              <button className="btn primary" onClick={playAgain}>Replay {report.island.name} with different choices</button>
              <Link className="btn" to="/new">Try another island</Link>
            </div>
          </div>
          <IslandArt island={report.island} sky="evening" mood={moodFromApproval(last.approval)} green={chosenGreen} smoke={0.5 + last.output_gap / 6} />
        </section>

        <section>
          <h2>Before and after</h2>
          <div className="tiles">
            {TILES.map((t) => {
              const from = t.start(start)
              const to = tileValues[t.key]
              const good = (to - from) * t.better > 0
              const flat = Math.abs(to - from) < 0.1
              return (
                <div key={t.key} className="tile panel">
                  <span className="tile-label">{t.label}</span>
                  <span className="tile-value">{t.fmt(to)}</span>
                  <span className={`tile-change ${flat ? '' : good ? 'good' : 'bad'}`}>
                    {flat ? 'unchanged' : `${good ? '✓' : '✗'} from ${t.fmt(from)}`}
                  </span>
                </div>
              )
            })}
          </div>
        </section>

        <section className="panel causes">
          <h2>Where the inflation came from</h2>
          <p className="muted">
            At its peak ({report.peak.quarter * 3} months in), inflation hit <strong>{report.peak.inflation.toFixed(1)}%</strong>.
            Here's how much each cause contributed, in percentage points:
          </p>
          <ul className="cause-list">
            {causes.map(([k, v]) => (
              <li key={k}>
                <div className="cause-head">
                  <span>{CAUSES[k][0]}</span>
                  <strong>{v >= 0 ? '+' : '−'}{Math.abs(v).toFixed(1)}</strong>
                </div>
                <span className="cause-track"><motion.span className={`cause-fill ${v < 0 ? 'neg' : ''}`} initial={{ width: 0 }} whileInView={{ width: `${(Math.abs(v) / maxCause) * 100}%` }} viewport={{ once: true }} /></span>
                <span className="muted small">{CAUSES[k][1]}</span>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>The consequence map</h2>
          <p className="lede">
            Each decision set off a chain of events. The chips show what that decision changed on its own: we replayed
            the two years with just that one choice swapped for the middle-of-the-road option.
          </p>
          <ol className="cmap">
            {report.consequence_map.map((c, idx) => (
              <motion.li key={c.card_id} className="cmap-item panel" initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-60px' }} transition={{ delay: 0.05 }}>
                <div className="cmap-head">
                  <span className="cmap-time">{c.time}</span>
                  <span className="cmap-card">{c.card_title}</span>
                </div>
                <h3><span aria-hidden>{c.icon}</span> {c.option_title}</h3>
                <div className="chain">
                  {c.chain.map((step, i) => (
                    <motion.div key={i} className={`chain-step ${i === 0 ? 'first' : ''}`} initial={{ opacity: 0, x: -10 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: 0.15 + i * 0.15 }}>
                      {step}
                    </motion.div>
                  ))}
                </div>
                {!c.was_baseline && (
                  <div className="cmap-impact">
                    <span className="small muted">This decision alone, compared to "{c.compared_to}":</span>
                    <ImpactChips items={c.impact} />
                  </div>
                )}
                {c.what_if && (
                  <details className="what-if">
                    <summary>What if you'd chosen <strong>{c.what_if.icon} {c.what_if.option_title}</strong> instead?</summary>
                    <ImpactChips items={c.what_if.impact} />
                  </details>
                )}
                <p className="history">📚 {c.history}</p>
                {idx < report.consequence_map.length - 1 && <span className="cmap-link" aria-hidden />}
              </motion.li>
            ))}
          </ol>
        </section>

        <section>
          <h2>The two years, quarter by quarter</h2>
          <div className="chart-grid">
            <LineChart title="Inflation" values={seriesOf(sim, 'inflation')} labels={labels} unit="%" target={sim.target_inflation} goodDirection="down" />
            <LineChart title="Unemployment" values={seriesOf(sim, 'unemployment')} labels={labels} unit="%" goodDirection="down" />
            <LineChart title={`${report.island.currency} value`} values={seriesOf(sim, 'currency_index')} labels={labels} format={(v) => v.toFixed(0)} goodDirection="up" />
            <LineChart title="Reserves (months of imports)" values={seriesOf(sim, 'reserves_months')} labels={labels} goodDirection="up" />
            <LineChart title="Government debt (% of GDP)" values={seriesOf(sim, 'debt_to_gdp')} labels={labels} format={(v) => v.toFixed(0)} goodDirection="down" />
            <LineChart title="Sustainability" values={seriesOf(sim, 'sustainability')} labels={labels} format={(v) => v.toFixed(0)} goodDirection="up" />
            <LineChart title={`${report.island.company.name} health`} values={seriesOf(sim, 'company_health')} labels={labels} format={(v) => v.toFixed(0)} goodDirection="up" />
            <LineChart title="Your approval" values={seriesOf(sim, 'approval')} labels={labels} unit="%" format={(v) => v.toFixed(0)} goodDirection="up" />
          </div>
        </section>

        <section className="two-col">
          <div className="panel">
            <h2>Where does money come from?</h2>
            <p className="muted">
              Most money isn't printed. It's created when banks make loans: a loan shows up as new money in the
              borrower's account. Higher interest rates mean fewer loans, so less new money. Printing adds central-bank
              money on top.
            </p>
            <div className="legend">
              <span><i className="sw bank" /> Created by bank lending</span>
              <span><i className="sw central" /> Created by the central bank</span>
            </div>
            {[['Before', start.money], ['After 2 years', last.money]].map(([label, m]) => {
              const total = m.bank + m.central
              const scale = Math.max(start.money.bank + start.money.central, last.money.bank + last.money.central)
              return (
                <div key={label} className="money-row">
                  <span className="money-label">{label}</span>
                  <span className="money-bar" style={{ width: `${(total / scale) * 100}%` }}>
                    <span className="bank" style={{ width: `${(m.bank / total) * 100}%` }} title={`Bank-created: ${m.bank.toFixed(0)}`} />
                    <span className="central" style={{ width: `${(m.central / total) * 100}%` }} title={`Central bank: ${m.central.toFixed(0)}`} />
                  </span>
                  <span className="money-total">{total.toFixed(0)}</span>
                </div>
              )
            })}
            <p className="small muted">
              The money supply grew by {moneyGrowth.toFixed(0)}%, while prices rose {sum.price_rise.toFixed(0)}%.
              {sum.price_rise > moneyGrowth + 10 && ' Prices outran the money: once people stop trusting a currency, they spend it the moment they get it, so the same money changes hands faster and pushes prices up again and again.'}
            </p>
          </div>

          <div className="panel">
            <h2>The shopping basket</h2>
            <p className="muted">What everyday things cost, in {currencySym}.</p>
            <table className="basket">
              <thead><tr><th>Item</th><th>Before</th><th>After</th><th>Change</th></tr></thead>
              <tbody>
                {[['bread', '🍞 Loaf of bread'], ['fuel', '⛽ Litre of petrol'], ['rent', '🏠 Monthly rent'], ['phone', '📱 Imported phone']].map(([k, name]) => {
                  const a = start.basket[k], b = last.basket[k]
                  const pct = (b / a - 1) * 100
                  return (
                    <tr key={k}>
                      <td>{name}</td>
                      <td>{a.toFixed(2)}</td>
                      <td>{b.toFixed(2)}</td>
                      <td className={pct > 0.5 ? 'bad' : 'good'}>{pct >= 0 ? '+' : ''}{pct.toFixed(0)}%</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2>The people of {report.island.name}</h2>
          <div className="citizen-grid">
            {report.citizens.map((c) => (
              <div key={c.id} className="citizen panel">
                <Portrait kind={c.avatar} size={72} mood={c.wellbeing} label={c.name} />
                <div>
                  <strong>{c.name}</strong>
                  <span className="muted small"> · {c.role}</span>
                  <p className="quote">"{c.quote}"</p>
                  <span className="mood-bar wide"><span style={{ width: `${c.wellbeing}%` }} className={c.wellbeing < 38 ? 'low' : c.wellbeing >= 62 ? 'high' : ''} /></span>
                  <span className="muted small">Wellbeing {Math.round(c.wellbeing)}/100</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="report-footer panel">
          <h2>Ready for another term?</h2>
          <p>Try the opposite of what you did and compare. That's the quickest way to see what each choice really does.</p>
          <div className="hero-actions">
            <button className="btn primary" onClick={playAgain}>Replay {report.island.name}</button>
            <Link className="btn" to="/new">Try another island</Link>
            <Link className="btn ghost" to="/">All my terms</Link>
          </div>
        </section>
      </main>
    </div>
  )
}
