import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../auth'
import IslandArt from '../components/IslandArt'

const PREVIEW = { id: 'coralia', name: 'Coralia', art: { buildings: 'town', palette: ['#ffb4a2', '#e5989b', '#6d6875'], size: 0.85 } }

export default function Login() {
  const { user, signIn } = useAuth()
  const navigate = useNavigate()
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  if (user) return <Navigate to="/" replace />

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })
  const submit = async (e) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const body = mode === 'register' ? form : { username: form.username, password: form.password }
      await signIn(mode, body)
      navigate('/')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-hero">
        <motion.h1 initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>Town Hall</motion.h1>
        <p className="lede">
          For one day, you run the economy of an island. A war breaks out, prices spike and everyone wants something
          from you. Make your calls, then watch the next two years play out and see what your choices really did.
        </p>
        <IslandArt island={PREVIEW} sky="noon" mood="cheer" boats={3} className="login-island" />
      </div>

      <motion.form className="panel login-card" onSubmit={submit} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
        <div className="tabs" role="tablist">
          <button type="button" role="tab" aria-selected={mode === 'login'} className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>Sign in</button>
          <button type="button" role="tab" aria-selected={mode === 'register'} className={mode === 'register' ? 'active' : ''} onClick={() => setMode('register')}>Create account</button>
        </div>
        <label>
          {mode === 'login' ? 'Username or email' : 'Username'}
          <input value={form.username} onChange={set('username')} autoComplete="username" required minLength={mode === 'register' ? 3 : 1} />
        </label>
        {mode === 'register' && (
          <label>
            Email
            <input type="email" value={form.email} onChange={set('email')} autoComplete="email" required />
          </label>
        )}
        <label>
          Password
          <input type="password" value={form.password} onChange={set('password')} autoComplete={mode === 'register' ? 'new-password' : 'current-password'} required minLength={mode === 'register' ? 8 : 1} />
        </label>
        {mode === 'register' && <p className="hint">At least 8 characters.</p>}
        {error && <p className="error" role="alert">{error}</p>}
        <button className="btn primary big" disabled={busy}>
          {busy ? 'One moment…' : mode === 'login' ? 'Enter the Town Hall' : 'Take the oath'}
        </button>
      </motion.form>
    </div>
  )
}
