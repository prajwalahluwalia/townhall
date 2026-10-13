import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { api, getToken, setToken } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (!getToken()) {
      setReady(true)
      return
    }
    api
      .me()
      .then(setUser)
      .catch(() => setToken(null))
      .finally(() => setReady(true))
  }, [])

  const signIn = useCallback(async (mode, body) => {
    const res = mode === 'register' ? await api.register(body) : await api.login(body)
    setToken(res.token)
    setUser(res.user)
  }, [])

  const signOut = useCallback(() => {
    setToken(null)
    setUser(null)
  }, [])

  return <AuthContext.Provider value={{ user, ready, signIn, signOut }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
