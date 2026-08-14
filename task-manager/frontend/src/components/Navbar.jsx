import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <nav className="border-b border-blueprint-line/15 bg-blueprint-900/80 backdrop-blur sticky top-0 z-30">
      <div className="max-w-6xl mx-auto px-5 py-3.5 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded border border-blueprint-line/50 flex items-center justify-center">
            <div className="w-2.5 h-2.5 border border-blueprint-line rounded-sm" />
          </div>
          <span className="font-display font-semibold text-paper text-lg">TaskFlow</span>
        </Link>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span
              className="w-6 h-6 rounded-full flex items-center justify-center text-[11px] font-mono text-blueprint-950 font-semibold"
              style={{ backgroundColor: user?.avatar_color || '#6EC6FF' }}
            >
              {user?.username?.[0]?.toUpperCase()}
            </span>
            <span className="text-sm text-slate-light hidden sm:inline">{user?.username}</span>
          </div>
          <button
            onClick={() => { logout(); navigate('/login') }}
            className="text-xs font-mono tracking-wide text-slate-light hover:text-blueprint-line border border-blueprint-line/20 hover:border-blueprint-line/50 rounded px-3 py-1.5 transition-colors"
          >
            SIGN OUT
          </button>
        </div>
      </div>
    </nav>
  )
}
