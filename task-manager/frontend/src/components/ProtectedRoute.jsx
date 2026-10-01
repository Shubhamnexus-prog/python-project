import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-blueprint-900">
        <div className="font-mono text-blueprint-line text-sm tracking-widest animate-pulse">
          LOADING SPEC...
        </div>
      </div>
    )
  }

  if (!user) return <Navigate to="/login" replace />
  return children
}
