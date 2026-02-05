# from __future__ import annotations
# from app.api.v1.todos import router as todos_router


# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse

# from app.api.v1.todos import router as todos_router
# from app.config.settings import get_settings
# from app.db.session import init_db
# from app.observability.logging import configure_logging

# settings = get_settings()

# app = FastAPI(title="Phase II Todo API", version="0.1.0")

# configure_logging(settings.log_level)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.middleware("http")
# async def inject_request_id(request: Request, call_next):
#     request_id = request.headers.get(settings.request_id_header)
#     response = await call_next(request)
#     if request_id:
#         response.headers[settings.request_id_header] = request_id
#     return response


# @app.on_event("startup")
# async def startup_event() -> None:
#     init_db()


# # ✅ Root endpoint
# @app.get("/")
# async def root() -> dict[str, str]:
#     return {
#         "message": "Phase II Todo API is running 🚀",
#         "docs": "/docs",
#         "health": "/healthz"
#     }


# # ✅ Health check
# @app.get("/healthz")
# async def healthcheck() -> dict[str, str]:
#     return {"status": "ok ✅"}


# # ✅ Favicon (404 error khatam ho jayega)
# @app.get("/favicon.ico")
# async def favicon():
#     return FileResponse("favicon.ico")


# # ✅ Routers
# app.include_router(todos_router, prefix="/api/v1")


from __future__ import annotations
import os
from dotenv import load_dotenv

# Load .env file FIRST before any other imports
load_dotenv()

# Set environment variables if not set
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:///./todos.db"
if not os.getenv("UNDO_TOKEN_SECRET"):
    os.environ["UNDO_TOKEN_SECRET"] = "your_secret_key_here_minimum_32_characters_long_for_security"
if not os.getenv("REQUEST_ID_HEADER"):
    os.environ["REQUEST_ID_HEADER"] = "X-Request-ID"
if not os.getenv("LOG_LEVEL"):
    os.environ["LOG_LEVEL"] = "INFO"

# NOW import the rest
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.v1.todos import router as todos_router
from app.config.settings import get_settings
from app.db.session import init_db
from app.observability.logging import configure_logging

settings = get_settings()

app = FastAPI(title="Phase II Todo API", version="0.1.0")

configure_logging(settings.log_level)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def inject_request_id(request: Request, call_next):
    request_id = request.headers.get(settings.request_id_header)
    response = await call_next(request)
    if request_id:
        response.headers[settings.request_id_header] = request_id
    return response


@app.on_event("startup")
async def startup_event() -> None:
    init_db()


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "Phase II Todo API is running 🚀",
        "docs": "/docs",
        "health": "/healthz"
    }


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok ✅"}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")


app.include_router(todos_router, prefix="/api/v1")