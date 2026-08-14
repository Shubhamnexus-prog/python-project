import { useEffect, useState, useMemo } from 'react'
import { useParams, Link } from 'react-router-dom'
import { DragDropContext, Droppable } from '@hello-pangea/dnd'
import api from '../api/axios'
import Navbar from '../components/Navbar'
import TaskCard from '../components/TaskCard'
import TaskModal from '../components/TaskModal'

const COLUMNS = [
  { key: 'todo', label: 'To Do' },
  { key: 'in_progress', label: 'In Progress' },
  { key: 'review', label: 'In Review' },
  { key: 'done', label: 'Done' },
]

export default function ProjectBoard() {
  const { id } = useParams()
  const [project, setProject] = useState(null)
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTask, setActiveTask] = useState(null)
  const [showNew, setShowNew] = useState(false)
  const [inviteUsername, setInviteUsername] = useState('')
  const [inviteError, setInviteError] = useState('')

  const load = async () => {
    const [projectRes, tasksRes] = await Promise.all([
      api.get(`/projects/${id}/`),
      api.get(`/tasks/?project=${id}`),
    ])
    setProject(projectRes.data)
    setTasks(tasksRes.data.results ?? tasksRes.data)
    setLoading(false)
  }

  useEffect(() => { load() }, [id])

  const columns = useMemo(() => {
    const grouped = {}
    COLUMNS.forEach((c) => (grouped[c.key] = []))
    tasks
      .slice()
      .sort((a, b) => a.order - b.order)
      .forEach((t) => grouped[t.status]?.push(t))
    return grouped
  }, [tasks])

  const handleDragEnd = async (result) => {
    const { source, destination, draggableId } = result
    if (!destination) return
    if (source.droppableId === destination.droppableId && source.index === destination.index) return

    const taskId = Number(draggableId)
    const newStatus = destination.droppableId

    // Optimistic local update
    setTasks((prev) => {
      const moved = prev.find((t) => t.id === taskId)
      const withoutMoved = prev.filter((t) => t.id !== taskId)
      const destTasks = withoutMoved
        .filter((t) => t.status === newStatus)
        .sort((a, b) => a.order - b.order)
      destTasks.splice(destination.index, 0, { ...moved, status: newStatus })

      const reindexed = destTasks.map((t, i) => ({ ...t, order: i }))
      const others = withoutMoved.filter((t) => t.status !== newStatus)
      return [...others, ...reindexed]
    })

    const destTasksForPayload = [
      ...columns[newStatus].filter((t) => t.id !== taskId),
    ]
    destTasksForPayload.splice(destination.index, 0, { id: taskId })
    const payload = destTasksForPayload.map((t, i) => ({ id: t.id, status: newStatus, order: i }))

    try {
      await api.post('/tasks/reorder/', payload)
    } catch {
      load() // reconcile with server on failure
    }
  }

  const handleTaskSaved = (saved) => {
    setTasks((prev) => {
      const exists = prev.some((t) => t.id === saved.id)
      return exists ? prev.map((t) => (t.id === saved.id ? saved : t)) : [saved, ...prev]
    })
    setActiveTask(null)
    setShowNew(false)
  }

  const handleTaskDeleted = (taskId) => {
    setTasks((prev) => prev.filter((t) => t.id !== taskId))
    setActiveTask(null)
  }

  const handleInvite = async (e) => {
    e.preventDefault()
    setInviteError('')
    try {
      const { data } = await api.post(`/projects/${id}/invite/`, { username: inviteUsername })
      setProject(data)
      setInviteUsername('')
    } catch (err) {
      setInviteError(err.response?.data?.username?.[0] || err.response?.data?.detail || 'Could not invite user.')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-blueprint-900 flex items-center justify-center">
        <div className="font-mono text-blueprint-line text-sm tracking-widest animate-pulse">LOADING BOARD...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-blueprint-900 bg-grid-blueprint bg-grid">
      <Navbar />
      <div className="max-w-7xl mx-auto px-5 py-8">
        <div className="flex items-start justify-between mb-6 flex-wrap gap-4">
          <div>
            <Link to="/" className="font-mono text-xs text-slate-light hover:text-blueprint-line">← ALL PROJECTS</Link>
            <div className="flex items-center gap-2.5 mt-2">
              <span className="w-3 h-3 rounded-sm" style={{ backgroundColor: project.color }} />
              <h1 className="font-display text-2xl font-semibold text-paper">{project.name}</h1>
            </div>
            {project.description && (
              <p className="text-slate-light text-sm mt-1 max-w-xl">{project.description}</p>
            )}
          </div>

          <div className="flex items-center gap-3">
            <div className="flex -space-x-1.5">
              {project.members.map((m) => (
                <span key={m.id} title={m.username}
                  className="w-7 h-7 rounded-full border-2 border-blueprint-900 flex items-center justify-center text-[10px] font-mono text-blueprint-950 font-semibold"
                  style={{ backgroundColor: m.avatar_color }}>
                  {m.username[0].toUpperCase()}
                </span>
              ))}
            </div>
            <button onClick={() => setShowNew(true)}
              className="bg-blueprint-line text-blueprint-950 font-medium text-sm px-4 py-2.5 rounded hover:bg-white transition-colors">
              + New task
            </button>
          </div>
        </div>

        <form onSubmit={handleInvite} className="flex items-center gap-2 mb-6">
          <input
            value={inviteUsername}
            onChange={(e) => setInviteUsername(e.target.value)}
            placeholder="Invite teammate by username…"
            className="bg-blueprint-800/60 border border-blueprint-line/20 rounded px-3 py-1.5 text-sm text-paper focus:outline-none focus:border-blueprint-line w-64"
          />
          <button type="submit" className="font-mono text-xs text-blueprint-line border border-blueprint-line/30 rounded px-3 py-1.5 hover:border-blueprint-line transition-colors">
            INVITE
          </button>
          {inviteError && <span className="text-xs text-signal-urgent">{inviteError}</span>}
        </form>

        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
            {COLUMNS.map((col) => (
              <div key={col.key} className="bg-blueprint-800/30 border border-blueprint-line/10 rounded-md p-3 flex flex-col">
                <div className="flex items-center justify-between mb-3 px-1">
                  <span className="font-mono text-xs tracking-wider text-blueprint-line">{col.label.toUpperCase()}</span>
                  <span className="font-mono text-[10px] text-slate-light bg-blueprint-900/50 rounded-full px-2 py-0.5">
                    {columns[col.key].length}
                  </span>
                </div>
                <Droppable droppableId={col.key}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      className={`space-y-2.5 min-h-[120px] flex-1 rounded transition-colors ${
                        snapshot.isDraggingOver ? 'bg-blueprint-line/5' : ''
                      }`}
                    >
                      {columns[col.key].map((task, index) => (
                        <TaskCard key={task.id} task={task} index={index} onClick={() => setActiveTask(task)} />
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            ))}
          </div>
        </DragDropContext>
      </div>

      {activeTask && (
        <TaskModal
          task={activeTask}
          projectId={project.id}
          members={project.members}
          onClose={() => setActiveTask(null)}
          onSaved={handleTaskSaved}
          onDeleted={handleTaskDeleted}
        />
      )}
      {showNew && (
        <TaskModal
          projectId={project.id}
          members={project.members}
          onClose={() => setShowNew(false)}
          onSaved={handleTaskSaved}
        />
      )}
    </div>
  )
}
