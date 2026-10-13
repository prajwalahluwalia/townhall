import { Link } from 'react-router-dom'
import GlossaryButton from './GlossaryButton'

export default function TopBar({ children, actions }) {
  return (
    <header className="topbar">
      <Link to="/" className="brand">
        <img src="/favicon.svg" alt="" width="28" height="28" />
        Town Hall
      </Link>
      <div className="topbar-middle">{children}</div>
      {/* The signed-in player's name and a sign-out button went here while accounts were on. */}
      <div className="topbar-actions">
        {actions}
        <GlossaryButton />
      </div>
    </header>
  )
}
