from fastapi import FastAPI

from src.api.routers import sessions

app = FastAPI(
    title="AgendaPro API",
    description="API de agendamento inteligente para professores.",
    version="0.1.0",
)

app.include_router(sessions.router)
