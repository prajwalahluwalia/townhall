import { useEffect, useState } from 'react'

export default function MobileWarning() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      // Hide warning in landscape (width > height) or if width > 640
      const isLandscape = window.innerWidth > window.innerHeight
      const isWideEnough = window.innerWidth > 640
      setIsMobile(!isLandscape && !isWideEnough)
    }
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  if (!isMobile) return null

  return (
    <div className="mobile-warning">
      <div className="mobile-warning-content">
        <h2>Desktop Only</h2>
        <p>Best on screens 12" and up</p>
        <ul>
          <li>💻 Laptop or Desktop</li>
          <li>🖥️ Browser Desktop Mode</li>
        </ul>
      </div>
    </div>
  )
}
