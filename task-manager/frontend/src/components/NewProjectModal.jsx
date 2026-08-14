import { useState } from 'react'

const COLORS = ['#0F2A4A', '#E8A33D', '#5FB88A', '#E15B4F', '#6EC6FF', '#8A5FB8']

export default function NewProjectModal({ onClose, onCreate }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [color, setColor] = useState(COLORS[0])
  const [busy, setBusy] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setBusy(true)
    try {
      await onCreate({ name, description, color })
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-blueprint-950/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">
      <form
        onSubmit={submit}
        className="blueprint-corners w-full max-w-md bg-blueprint-800 border border-blueprint-line/25 rounded-md p-6 space-y-4"
      >
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs tracking-[0.25em] text-blueprint-line">NEW SPEC — PROJECT</span>
          <button type="button" onClick={onClose} className="text-slate-light hover:text-paper text-lg leading-none">×</button>
        </div>
        <div>
          <label className="block text-xs font-mono text-blueprint-line/80 mb-1">NAME</label>
          <input
            required autoFocus value={name} onChange={(e) => setName(e.target.value)}
            className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line"
            placeholder="Website Revamp"
          />
        </div>
        <div>
          <label className="block text-xs font-mono text-blueprint-line/80 mb-1">DESCRIPTION</label>
          <textarea
            value={description} onChange={(e) => setDescription(e.target.value)} rows={3}
            className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line resize-none"
            placeholder="What's this project about?"
          />
        </div>
        <div>
          <label className="block text-xs font-mono text-blueprint-line/80 mb-2">COLOR TAG</label>
          <div className="flex gap-2">
            {COLORS.map((c) => (
              <button
                type="button" key={c} onClick={() => setColor(c)}
                className={`w-7 h-7 rounded-full border-2 transition-transform ${color === c ? 'scale-110 border-white' : 'border-transparent'}`}
                style={{ backgroundColor: c }}
              />
            ))}
          </div>
        </div>
        <button
          type="submit" disabled={busy}
          className="w-full bg-blueprint-line text-blueprint-950 font-medium text-sm py-2.5 rounded hover:bg-white transition-colors disabled:opacity-50"
        >
          {busy ? 'Creating…' : 'Create project'}
        </button>
      </form>
    </div>
  )
}
