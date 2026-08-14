import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({ baseURL: API_BASE_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('taskflow_access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let queue = []

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('taskflow_refresh')
      if (!refresh) {
        localStorage.removeItem('taskflow_access')
        window.location.href = '/login'
        return Promise.reject(error)
      }
      if (isRefreshing) {
        return new Promise((resolve) => queue.push(resolve)).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }
      isRefreshing = true
      try {
        const { data } = await axios.post(`${API_BASE_URL}/auth/login/refresh/`, { refresh })
        localStorage.setItem('taskflow_access', data.access)
        queue.forEach((resolve) => resolve(data.access))
        queue = []
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch (e) {
        localStorage.removeItem('taskflow_access')
        localStorage.removeItem('taskflow_refresh')
        window.location.href = '/login'
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)

export default api
