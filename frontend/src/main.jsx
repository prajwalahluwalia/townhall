import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import IslandSelect from './pages/IslandSelect'
import Game from './pages/Game'
import FastForward from './pages/FastForward'
import Report from './pages/Report'
import './styles.css'

// Accounts and saved games are switched off for now: anyone can play straight away.
// To bring them back, wrap the app in <AuthProvider> from './auth', restore the /login and
// home routes (pages/Login.jsx, pages/Home.jsx), and guard the game routes behind a login.

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<IslandSelect />} />
        <Route path="/play" element={<Game />} />
        <Route path="/play/forward" element={<FastForward />} />
        <Route path="/play/report" element={<Report />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
