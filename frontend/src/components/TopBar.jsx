import { Link } from 'react-router-dom'
import { useAuth } from '../auth'

export default function TopBar({ children }) {
  const { user, signOut } = useAuth()
  return (
    <header className="topbar">
      <Link to="/" className="brand">
        <img src="/favicon.svg" alt="" width="28" height="28" />
        Town Hall
      </Link>
      <div className="topbar-middle">{children}</div>
      {user && (
        <div className="topbar-user">
          <span className="muted">{user.username}</span>
          <button className="btn ghost small" onClick={signOut}>Sign out</button>
        </div>
      )}
    </header>
  )
}
