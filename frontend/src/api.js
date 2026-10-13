const TOKEN_KEY = 'townhall_token'

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    /* storage unavailable: the session just won't survive a reload */
  }
}

export class ApiError extends Error {
  constructor(status, message) {
    super(message)
    this.status = status
  }
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`/api${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  if (res.status === 204) return null
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    let message = data.detail
    if (Array.isArray(message)) message = message.map((d) => d.msg.replace(/^Value error, /, '')).join('. ')
    throw new ApiError(res.status, message || `Request failed (${res.status})`)
  }
  return data
}

export const api = {
  islands: () => request('GET', '/islands'),
  // Play without an account: send the game along, the server saves nothing.
  play: (play) => request('POST', '/play', play),
  decide: (play, cardId, optionId) => request('POST', '/play/decide', { ...play, card_id: cardId, option_id: optionId }),
  report: (play) => request('POST', '/play/report', play),
}

// Accounts and saved games, switched off for now (see backend/app/main.py).
export const accountsApi = {
  register: (body) => request('POST', '/auth/register', body),
  login: (body) => request('POST', '/auth/login', body),
  me: () => request('GET', '/auth/me'),
  games: () => request('GET', '/games'),
  newGame: (islandId, scenarioId) => request('POST', '/games', { island_id: islandId, scenario_id: scenarioId }),
  game: (id) => request('GET', `/games/${id}`),
  decide: (id, cardId, optionId) => request('POST', `/games/${id}/decisions`, { card_id: cardId, option_id: optionId }),
  fastForward: (id) => request('POST', `/games/${id}/fast-forward`),
  report: (id) => request('GET', `/games/${id}/report`),
  deleteGame: (id) => request('DELETE', `/games/${id}`),
}
