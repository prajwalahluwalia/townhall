import { useState } from 'react'
import { GLOSSARY } from '../glossary'
import Modal from './Modal'

export default function GlossaryButton() {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const q = query.trim().toLowerCase()
  const entries = [...GLOSSARY]
    .sort((a, b) => a.term.localeCompare(b.term))
    .filter((e) => !q || e.term.toLowerCase().includes(q) || e.text.toLowerCase().includes(q))
  return (
    <>
      <button className="btn small" onClick={() => setOpen(true)}>📖 Words</button>
      {open && (
        <Modal title="What do these words mean?" onClose={() => setOpen(false)} wide>
          <p className="muted">Underlined words in the game have explanations too: hover or tap them.</p>
          <input type="search" placeholder="Search, e.g. GDP or lender" value={query} onChange={(e) => setQuery(e.target.value)} autoFocus />
          <dl className="glossary-list">
            {entries.map((e) => (
              <div key={e.id}>
                <dt>{e.term}</dt>
                <dd>{e.text}{e.example && <em> {e.example}</em>}</dd>
              </div>
            ))}
            {entries.length === 0 && <p className="muted">No word matches "{query}".</p>}
          </dl>
        </Modal>
      )}
    </>
  )
}
