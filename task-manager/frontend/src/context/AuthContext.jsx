import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('taskflow_access')
    if (!token) {
      setLoading(false)
      return
    }
    api
      .get('/auth/me/')
      .then((res) => setUser(res.data))
      .catch(() => {
        localStorage.removeItem('taskflow_access')
        localStorage.removeItem('taskflow_refresh')
      })
      .finally(() => setLoading(false))
  }, [])

  const login = async (username, password) => {
    const { data } = await api.post('/auth/login/', { username, password })
    localStorage.setItem('taskflow_access', data.access)
    localStorage.setItem('taskflow_refresh', data.refresh)
    setUser(data.user)
    return data.user
  }

  const register = async (payload) => {
    const { data } = await api.post('/auth/register/', payload)
    localStorage.setItem('taskflow_access', data.access)
    localStorage.setItem('taskflow_refresh', data.refresh)
    setUser(data.user)
    return data.user
  }

  const logout = () => {
    localStorage.removeItem('taskflow_access')
    localStorage.removeItem('taskflow_refresh')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
