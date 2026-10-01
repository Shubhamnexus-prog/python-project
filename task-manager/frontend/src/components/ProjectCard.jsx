import { Link } from 'react-router-dom'

export default function ProjectCard({ project }) {
  const pct = project.task_count
    ? Math.round((project.done_count / project.task_count) * 100)
    : 0

  return (
    <Link
      to={`/projects/${project.id}`}
      className="blueprint-corners group block bg-blueprint-800/50 border border-blueprint-line/15 hover:border-blueprint-line/50 rounded-md p-5 transition-colors"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-sm" style={{ backgroundColor: project.color }} />
          <span className="font-mono text-[10px] tracking-widest text-slate-light">
            PRJ-{String(project.id).padStart(3, '0')}
          </span>
        </div>
        <span className="font-mono text-[10px] text-slate-light">{pct}% DONE</span>
      </div>

      <h3 className="font-display text-lg font-semibold text-paper mb-1.5 group-hover:text-blueprint-line transition-colors">
        {project.name}
      </h3>
      <p className="text-sm text-slate-light line-clamp-2 min-h-[2.5rem]">
        {project.description || 'No description yet.'}
      </p>

      <div className="mt-4 h-1 bg-blueprint-900 rounded-full overflow-hidden">
        <div
          className="h-full bg-blueprint-line transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="mt-3 flex items-center justify-between text-xs text-slate-light">
        <span>{project.task_count} task{project.task_count !== 1 ? 's' : ''}</span>
        <span className="flex -space-x-1.5">
          {project.members.slice(0, 4).map((m) => (
            <span
              key={m.id}
              title={m.username}
              className="w-5 h-5 rounded-full border border-blueprint-900 flex items-center justify-center text-[9px] font-mono text-blueprint-950 font-semibold"
              style={{ backgroundColor: m.avatar_color }}
            >
              {m.username[0].toUpperCase()}
            </span>
          ))}
        </span>
      </div>
    </Link>
  )
}
