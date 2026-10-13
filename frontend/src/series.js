// Helpers to turn the simulation timeline into chart series. Index 0 is the
// starting point (the morning of day 1); indexes 1..8 are the quarters after.

const START_KEYS = {
  approval: 'approval_after_day',
}

export function seriesOf(sim, key) {
  const start = sim.start[START_KEYS[key] || key]
  return [start, ...sim.timeline.map((q) => q[key])]
}

export function quarterLabels(n) {
  return ['Start', ...Array.from({ length: n }, (_, i) => `${(i + 1) * 3}m`)]
}

export function skyForTime(time) {
  const h = parseInt(time, 10)
  if (h < 9) return 'dawn'
  if (h < 13) return 'noon'
  if (h < 17) return 'afternoon'
  if (h < 19) return 'evening'
  return 'night'
}

export function moodFromApproval(a) {
  return a >= 55 ? 'cheer' : a < 38 ? 'boo' : 'mixed'
}
