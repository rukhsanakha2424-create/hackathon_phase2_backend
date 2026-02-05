import os
from collections.abc import Generator
from sqlmodel import Session, SQLModel, create_engine

# Set default environment variables if not set
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:///./todos.db"
if not os.getenv("UNDO_TOKEN_SECRET"):
    os.environ["UNDO_TOKEN_SECRET"] = "your_secret_key_here_minimum_32_characters_long"

from app.config.settings import get_settings

settings = get_settings()
connect_args = {"check_same_thread": False} if "sqlite" in str(settings.database_url) else {}

engine = create_engine(
    str(settings.database_url),
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session