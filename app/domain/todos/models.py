from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=140)
    notes: str | None = Field(default=None, max_length=500)
    priority: Priority = Field(default=Priority.medium)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = Field(default=None)
