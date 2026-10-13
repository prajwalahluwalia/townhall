import { AnimatePresence, motion } from 'framer-motion'

const STATS = [
  { key: 'approval', label: 'Approval', icon: '👥', fmt: (v) => `${Math.round(v)}%`, meter: true, better: 1 },
  { key: 'inflation', label: 'Inflation', icon: '🔥', fmt: (v) => `${v.toFixed(1)}%`, better: -1 },
  { key: 'interest_rate', label: 'Interest rate', icon: '🏦', fmt: (v) => `${v.toFixed(1)}%`, better: 0 },
  { key: 'currency_index', label: 'Currency', icon: '💱', fmt: (v) => v.toFixed(1), better: 1, hint: '100 = this morning' },
  { key: 'reserves_months', label: 'Reserves', icon: '🪙', fmt: (v) => `${v.toFixed(1)} mo`, better: 1, hint: 'Months of imports the bank can pay for' },
  { key: 'debt_to_gdp', label: 'Debt', icon: '📜', fmt: (v) => `${Math.round(v)}% GDP`, better: -1 },
]

export default function Hud({ stats, deltas = {}, currencyCode }) {
  return (
    <div className="hud" role="group" aria-label="Island dashboard">
      {STATS.map((s) => {
        const delta = deltas[s.key]
        const show = delta != null && Math.abs(delta) >= 0.05
        const good = s.better === 0 ? null : delta * s.better > 0
        return (
          <div className="hud-stat" key={s.key} title={s.hint || ''}>
            <span className="hud-icon" aria-hidden>{s.icon}</span>
            <div className="hud-body">
              <span className="hud-label">{s.key === 'currency_index' && currencyCode ? currencyCode : s.label}</span>
              <span className="hud-value">{s.fmt(stats[s.key])}</span>
              {s.meter && (
                <span className="meter"><span style={{ width: `${stats[s.key]}%` }} className={stats[s.key] < 35 ? 'low' : ''} /></span>
              )}
            </div>
            <AnimatePresence>
              {show && (
                <motion.span
                  key={`${s.key}-${delta}`}
                  className={`hud-delta ${good == null ? '' : good ? 'good' : 'bad'}`}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: -2 }}
                  exit={{ opacity: 0 }}
                >
                  {delta > 0 ? '+' : '−'}{Math.abs(delta) >= 10 ? Math.round(Math.abs(delta)) : Math.abs(delta).toFixed(1)}
                </motion.span>
              )}
            </AnimatePresence>
          </div>
        )
      })}
    </div>
  )
}
