import { useLayoutEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { splitTerms } from '../glossary'

// A word from the glossary: dotted underline, explanation on hover, focus or tap.
// `nested`: inside a button, so it can't be focusable on its own.
export function Term({ entry, children, nested = false }) {
  const ref = useRef(null)
  const tip = useRef(null)
  const [open, setOpen] = useState(false)
  const [pos, setPos] = useState(null)

  useLayoutEffect(() => {
    if (!open || !ref.current || !tip.current) return
    const r = ref.current.getBoundingClientRect()
    const t = tip.current.getBoundingClientRect()
    const left = Math.min(Math.max(8, r.left + r.width / 2 - t.width / 2), window.innerWidth - t.width - 8)
    const above = r.top - t.height - 8
    setPos({ left, top: above > 8 ? above : r.bottom + 8 })
  }, [open])

  return (
    <>
      <span ref={ref} className="term" tabIndex={nested ? undefined : 0} role={nested ? undefined : 'button'}
        aria-expanded={nested ? undefined : open}
        onMouseEnter={() => setOpen(true)} onMouseLeave={() => setOpen(false)}
        onFocus={() => setOpen(true)} onBlur={() => setOpen(false)}
        onClick={(e) => { e.stopPropagation(); e.preventDefault(); setOpen((o) => !o) }}
        onKeyDown={(e) => e.key === 'Escape' && setOpen(false)}>
        {children}
      </span>
      {open && createPortal(
        <span ref={tip} role="tooltip" className="term-tip" style={pos ? { left: pos.left, top: pos.top } : { visibility: 'hidden' }}>
          <strong>{entry.term}</strong>
          <span>{entry.text}</span>
          {entry.example && <em>{entry.example}</em>}
        </span>,
        document.body,
      )}
    </>
  )
}

// Text with every glossary word (first mention only) explained in place.
export default function Explain({ children, nested = false }) {
  if (typeof children !== 'string') return children
  return splitTerms(children).map((part, i) =>
    part.entry ? <Term key={i} entry={part.entry} nested={nested}>{part.text}</Term> : <span key={i}>{part.text}</span>,
  )
}
