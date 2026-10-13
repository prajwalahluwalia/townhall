import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth'
import Login from './pages/Login'
import Home from './pages/Home'
import IslandSelect from './pages/IslandSelect'
import Game from './pages/Game'
import FastForward from './pages/FastForward'
import Report from './pages/Report'
import './styles.css'

function Protected({ children }) {
  const { user, ready } = useAuth()
  if (!ready) return <div className="loading-screen">Opening the Town Hall…</div>
  if (!user) return <Navigate to="/login" replace />
  return children
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Protected><Home /></Protected>} />
          <Route path="/new" element={<Protected><IslandSelect /></Protected>} />
          <Route path="/game/:id" element={<Protected><Game /></Protected>} />
          <Route path="/game/:id/forward" element={<Protected><FastForward /></Protected>} />
          <Route path="/game/:id/report" element={<Protected><Report /></Protected>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  </StrictMode>,
)
