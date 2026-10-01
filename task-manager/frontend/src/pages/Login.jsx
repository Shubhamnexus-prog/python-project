import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      await login(username, password)
      navigate('/')
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Sign-in failed. Check your username and password.'
      )
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen bg-blueprint-900 bg-grid-blueprint bg-grid flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 text-blueprint-line font-mono text-xs tracking-[0.3em] mb-3">
            SPEC 01 — ACCESS
          </div>
          <h1 className="font-display text-3xl font-semibold text-paper">TaskFlow</h1>
          <p className="text-slate-light text-sm mt-1">Sign in to open the board.</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="blueprint-corners bg-blueprint-800/60 border border-blueprint-line/20 rounded-md p-6 space-y-4 backdrop-blur-sm"
        >
          {error && (
            <div className="text-sm text-signal-urgent bg-signal-urgent/10 border border-signal-urgent/30 rounded px-3 py-2">
              {error}
            </div>
          )}
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1 tracking-wide">
              USERNAME
            </label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line placeholder:text-slate"
              placeholder="jane_doe"
            />
          </div>
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1 tracking-wide">
              PASSWORD
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line placeholder:text-slate"
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            disabled={busy}
            className="w-full bg-blueprint-line text-blueprint-950 font-medium text-sm py-2.5 rounded hover:bg-white transition-colors disabled:opacity-50"
          >
            {busy ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="text-center text-sm text-slate-light mt-5">
          New here?{' '}
          <Link to="/register" className="text-blueprint-line hover:underline">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  )
}
