import { useEffect, useState } from 'react'
import api from '../api/axios'
import Navbar from '../components/Navbar'
import ProjectCard from '../components/ProjectCard'
import NewProjectModal from '../components/NewProjectModal'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const { user } = useAuth()

  const load = () => {
    api.get('/projects/').then((res) => {
      setProjects(res.data.results ?? res.data)
      setLoading(false)
    })
  }

  useEffect(load, [])

  const handleCreate = async (payload) => {
    const { data } = await api.post('/projects/', payload)
    setProjects((prev) => [data, ...prev])
    setShowModal(false)
  }

  return (
    <div className="min-h-screen bg-blueprint-900 bg-grid-blueprint bg-grid">
      <Navbar />
      <div className="max-w-6xl mx-auto px-5 py-10">
        <div className="flex items-end justify-between mb-8">
          <div>
            <div className="font-mono text-xs tracking-[0.3em] text-blueprint-line mb-2">
              WORKSPACE — {user?.username?.toUpperCase()}
            </div>
            <h1 className="font-display text-3xl font-semibold text-paper">Your Projects</h1>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blueprint-line text-blueprint-950 font-medium text-sm px-4 py-2.5 rounded hover:bg-white transition-colors"
          >
            + New project
          </button>
        </div>

        {loading ? (
          <div className="font-mono text-sm text-slate-light">Loading projects…</div>
        ) : projects.length === 0 ? (
          <div className="blueprint-corners border border-dashed border-blueprint-line/25 rounded-md p-16 text-center">
            <p className="text-slate-light text-sm mb-4">
              No projects on the board yet. Start your first spec.
            </p>
            <button
              onClick={() => setShowModal(true)}
              className="bg-blueprint-line text-blueprint-950 font-medium text-sm px-4 py-2.5 rounded hover:bg-white transition-colors"
            >
              + New project
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {projects.map((p) => (
              <ProjectCard key={p.id} project={p} />
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <NewProjectModal onClose={() => setShowModal(false)} onCreate={handleCreate} />
      )}
    </div>
  )
}
