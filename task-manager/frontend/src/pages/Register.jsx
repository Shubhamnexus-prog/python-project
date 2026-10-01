import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [form, setForm] = useState({
    username: '', email: '', password: '', password2: '',
  })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      await register(form)
      navigate('/')
    } catch (err) {
      const data = err.response?.data
      const firstError = data && Object.values(data)[0]
      setError(Array.isArray(firstError) ? firstError[0] : firstError || 'Registration failed.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen bg-blueprint-900 bg-grid-blueprint bg-grid flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 text-blueprint-line font-mono text-xs tracking-[0.3em] mb-3">
            SPEC 02 — NEW ACCOUNT
          </div>
          <h1 className="font-display text-3xl font-semibold text-paper">TaskFlow</h1>
          <p className="text-slate-light text-sm mt-1">Draft your workspace in seconds.</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="blueprint-corners bg-blueprint-800/60 border border-blueprint-line/20 rounded-md p-6 space-y-3.5 backdrop-blur-sm"
        >
          {error && (
            <div className="text-sm text-signal-urgent bg-signal-urgent/10 border border-signal-urgent/30 rounded px-3 py-2">
              {error}
            </div>
          )}
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1 tracking-wide">USERNAME</label>
            <input required value={form.username} onChange={update('username')}
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
          </div>
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1 tracking-wide">EMAIL</label>
            <input type="email" required value={form.email} onChange={update('email')}
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
          </div>
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1 tracking-wide">PASSWORD</label>
            <input type="password" required value={form.password} onChange={update('password')}
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
          </div>
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1 tracking-wide">CONFIRM PASSWORD</label>
            <input type="password" required value={form.password2} onChange={update('password2')}
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
          </div>
          <button type="submit" disabled={busy}
            className="w-full bg-blueprint-line text-blueprint-950 font-medium text-sm py-2.5 rounded hover:bg-white transition-colors disabled:opacity-50 !mt-5">
            {busy ? 'Creating account…' : 'Create account'}
          </button>
        </form>

        <p className="text-center text-sm text-slate-light mt-5">
          Already have an account?{' '}
          <Link to="/login" className="text-blueprint-line hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
