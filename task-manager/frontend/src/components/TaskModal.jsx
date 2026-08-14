import { useState, useEffect } from 'react'
import api from '../api/axios'

const STATUS_OPTIONS = [
  { value: 'todo', label: 'To Do' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'review', label: 'In Review' },
  { value: 'done', label: 'Done' },
]
const PRIORITY_OPTIONS = ['low', 'medium', 'high', 'urgent']

export default function TaskModal({ task, projectId, members, onClose, onSaved, onDeleted }) {
  const isEdit = Boolean(task)
  const [form, setForm] = useState({
    title: task?.title || '',
    description: task?.description || '',
    status: task?.status || 'todo',
    priority: task?.priority || 'medium',
    assignee_id: task?.assignee?.id || '',
    due_date: task?.due_date || '',
  })
  const [comments, setComments] = useState(task?.comments || [])
  const [newComment, setNewComment] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const payload = { ...form, assignee_id: form.assignee_id || null, due_date: form.due_date || null }
      if (isEdit) {
        const { data } = await api.patch(`/tasks/${task.id}/`, payload)
        onSaved(data)
      } else {
        const { data } = await api.post('/tasks/', { ...payload, project: projectId })
        onSaved(data)
      }
    } catch (err) {
      setError('Could not save the task. Check the fields and try again.')
    } finally {
      setBusy(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Delete this task? This cannot be undone.')) return
    await api.delete(`/tasks/${task.id}/`)
    onDeleted(task.id)
  }

  const postComment = async (e) => {
    e.preventDefault()
    if (!newComment.trim()) return
    const { data } = await api.post('/tasks/comments/', { task: task.id, body: newComment })
    setComments((prev) => [...prev, data])
    setNewComment('')
  }

  return (
    <div className="fixed inset-0 bg-blueprint-950/70 backdrop-blur-sm flex items-center justify-center z-50 px-4 py-8">
      <div className="blueprint-corners w-full max-w-lg max-h-[90vh] overflow-y-auto bg-blueprint-800 border border-blueprint-line/25 rounded-md p-6">
        <div className="flex items-center justify-between mb-5">
          <span className="font-mono text-xs tracking-[0.25em] text-blueprint-line">
            {isEdit ? `TSK-${String(task.id).padStart(3, '0')} — EDIT` : 'NEW SPEC — TASK'}
          </span>
          <button onClick={onClose} className="text-slate-light hover:text-paper text-lg leading-none">×</button>
        </div>

        {error && (
          <div className="text-sm text-signal-urgent bg-signal-urgent/10 border border-signal-urgent/30 rounded px-3 py-2 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={submit} className="space-y-3.5">
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1">TITLE</label>
            <input required value={form.title} onChange={update('title')}
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
          </div>
          <div>
            <label className="block text-xs font-mono text-blueprint-line/80 mb-1">DESCRIPTION</label>
            <textarea value={form.description} onChange={update('description')} rows={3}
              className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line resize-none" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-mono text-blueprint-line/80 mb-1">STATUS</label>
              <select value={form.status} onChange={update('status')}
                className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line">
                {STATUS_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-mono text-blueprint-line/80 mb-1">PRIORITY</label>
              <select value={form.priority} onChange={update('priority')}
                className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line">
                {PRIORITY_OPTIONS.map((p) => <option key={p} value={p}>{p[0].toUpperCase() + p.slice(1)}</option>)}
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-mono text-blueprint-line/80 mb-1">ASSIGNEE</label>
              <select value={form.assignee_id} onChange={update('assignee_id')}
                className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line">
                <option value="">Unassigned</option>
                {members.map((m) => <option key={m.id} value={m.id}>{m.username}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-mono text-blueprint-line/80 mb-1">DUE DATE</label>
              <input type="date" value={form.due_date || ''} onChange={update('due_date')}
                className="w-full bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
            </div>
          </div>

          <div className="flex gap-2 !mt-5">
            <button type="submit" disabled={busy}
              className="flex-1 bg-blueprint-line text-blueprint-950 font-medium text-sm py-2.5 rounded hover:bg-white transition-colors disabled:opacity-50">
              {busy ? 'Saving…' : isEdit ? 'Save changes' : 'Create task'}
            </button>
            {isEdit && (
              <button type="button" onClick={handleDelete}
                className="px-4 py-2.5 rounded border border-signal-urgent/40 text-signal-urgent text-sm hover:bg-signal-urgent/10 transition-colors">
                Delete
              </button>
            )}
          </div>
        </form>

        {isEdit && (
          <div className="mt-6 pt-5 border-t border-blueprint-line/15">
            <span className="font-mono text-xs tracking-[0.25em] text-blueprint-line block mb-3">
              COMMENTS ({comments.length})
            </span>
            <div className="space-y-3 max-h-40 overflow-y-auto mb-3">
              {comments.map((c) => (
                <div key={c.id} className="text-sm">
                  <span className="font-medium text-paper">{c.author.username}</span>
                  <span className="text-slate-light text-xs ml-2">
                    {new Date(c.created_at).toLocaleString()}
                  </span>
                  <p className="text-slate-light">{c.body}</p>
                </div>
              ))}
              {comments.length === 0 && (
                <p className="text-slate-light text-sm">No comments yet.</p>
              )}
            </div>
            <form onSubmit={postComment} className="flex gap-2">
              <input value={newComment} onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add a comment…"
                className="flex-1 bg-blueprint-900/70 border border-blueprint-line/25 rounded px-3 py-2 text-paper text-sm focus:outline-none focus:border-blueprint-line" />
              <button type="submit"
                className="px-3.5 py-2 rounded bg-blueprint-line/15 border border-blueprint-line/40 text-blueprint-line text-sm hover:bg-blueprint-line/25 transition-colors">
                Post
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  )
}
