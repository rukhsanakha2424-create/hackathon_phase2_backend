from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlmodel import Session, select

from app.domain.todos.models import Priority, Todo


class TodoNotFoundError(ValueError):
    pass


class TodoService:
    """Domain service applying Phase I semantics with SQLModel persistence."""

    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, *, title: str, notes: str | None, priority: Priority) -> Todo:
        todo = Todo(title=title, notes=notes, priority=priority)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def list_todos(self, *, status: str | None = None) -> Sequence[Todo]:
        statement = select(Todo).order_by(Todo.created_at.desc())
        if status == "completed":
            statement = statement.where(Todo.completed.is_(True))
        elif status == "pending":
            statement = statement.where(Todo.completed.is_(False))
        elif status not in (None, "all"):
            raise ValueError("status must be one of: completed, pending, all, or None")
        return list(self.session.exec(statement))

    def update_todo(
        self,
        todo_id: int,
        *,
        title: str | None,
        notes: str | None,
        priority: Priority | None,
    ) -> Todo:
        todo = self._get_todo(todo_id)
        changed = False
        if title is not None:
            todo.title = title
            changed = True
        if notes is not None:
            todo.notes = notes
            changed = True
        if priority is not None:
            todo.priority = priority
            changed = True
        if changed:
            todo.updated_at = datetime.utcnow()
            self.session.add(todo)
            self.session.commit()
            self.session.refresh(todo)
        return todo

    def toggle_completion(self, todo_id: int) -> Todo:
        todo = self._get_todo(todo_id)
        todo.completed = not todo.completed
        todo.completed_at = datetime.utcnow() if todo.completed else None
        todo.updated_at = datetime.utcnow()
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, todo_id: int) -> Todo:
        todo = self._get_todo(todo_id)
        self.session.delete(todo)
        self.session.commit()
        return todo

    def undo_delete(self, todo_id: int, token: str) -> Todo:
        raise NotImplementedError("Undo flow is deferred until token handling is defined")

    def _get_todo(self, todo_id: int) -> Todo:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        return todo
