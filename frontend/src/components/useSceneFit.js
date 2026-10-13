import { useLayoutEffect } from 'react'

// Sizes the island picture (.scene-box) in a column it shares with other panels. The picture is
// always as wide as the column; its height is its natural 400:280 height, capped to the room left
// above the other panels. Written to the column as --scene-h. When capped, the picture trims a
// little sky and sea at the top and bottom (never the sides), so the island stays whole.
export default function useSceneFit(ref) {
  useLayoutEffect(() => {
    const col = ref.current
    if (!col) return
    const update = () => {
      const kids = [...col.children]
      const scene = kids.find((k) => k.classList.contains('scene-box'))
      if (!scene) return
      const gap = parseFloat(getComputedStyle(col).rowGap) || 0
      const others = kids.filter((k) => k !== scene).reduce((h, k) => h + k.offsetHeight, 0) + gap * (kids.length - 1)
      const height = Math.floor(Math.max(120, Math.min((col.clientWidth * 280) / 400, col.clientHeight - others)))
      const prev = parseFloat(col.style.getPropertyValue('--scene-h'))
      if (!prev || Math.abs(prev - height) > 2) col.style.setProperty('--scene-h', `${height}px`)
    }
    const observer = new ResizeObserver(update)
    observer.observe(col)
    for (const kid of col.children) observer.observe(kid)
    update()
    return () => observer.disconnect()
  })
}
