import { Draggable } from '@hello-pangea/dnd'

const PRIORITY_COLOR = {
  low: 'bg-signal-low',
  medium: 'bg-signal-medium',
  high: 'bg-signal-high',
  urgent: 'bg-signal-urgent',
}

export default function TaskCard({ task, index, onClick }) {
  return (
    <Draggable draggableId={String(task.id)} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          onClick={onClick}
          className={`blueprint-corners bg-paper rounded-md p-3.5 cursor-pointer border transition-shadow ${
            snapshot.isDragging
              ? 'border-blueprint-line shadow-2xl rotate-1'
              : 'border-transparent hover:border-blueprint-line/40 shadow-sm'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] text-slate tracking-wider">
              TSK-{String(task.id).padStart(3, '0')}
            </span>
            <span className={`w-2 h-2 rounded-full ${PRIORITY_COLOR[task.priority]}`} title={task.priority} />
          </div>
          <p className="text-ink text-sm font-medium leading-snug mb-2.5">{task.title}</p>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {task.due_date && (
                <span className="font-mono text-[10px] text-slate">
                  {new Date(task.due_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </span>
              )}
              {task.comment_count > 0 && (
                <span className="font-mono text-[10px] text-slate">💬 {task.comment_count}</span>
              )}
            </div>
            {task.assignee && (
              <span
                className="w-5 h-5 rounded-full flex items-center justify-center text-[9px] font-mono font-semibold text-blueprint-950"
                style={{ backgroundColor: task.assignee.avatar_color }}
                title={task.assignee.username}
              >
                {task.assignee.username[0].toUpperCase()}
              </span>
            )}
          </div>
        </div>
      )}
    </Draggable>
  )
}
