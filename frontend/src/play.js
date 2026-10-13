// The current game lives only in this browser: which island, which crisis, and the choices so far.
// The server rebuilds everything else from that, so nothing about the player is stored anywhere.

const KEY = 'townhall_play'

export function loadPlay() {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY))
    if (saved?.island_id && saved?.scenario_id && Array.isArray(saved.decisions)) return saved
  } catch {
    /* storage unavailable or corrupted: start fresh */
  }
  return null
}

export function savePlay(play) {
  try {
    localStorage.setItem(KEY, JSON.stringify(play))
  } catch {
    /* storage unavailable: the game still works, it just won't survive a reload */
  }
  return play
}

export function newPlay(islandId, scenarioId) {
  return savePlay({ island_id: islandId, scenario_id: scenarioId, decisions: [] })
}
