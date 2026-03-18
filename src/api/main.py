import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.dependencies import get_client, get_session_repository
from src.api.routers import appointments, professors, sessions
from src.application.use_cases.expire_session_locks import ExpireSessionLocksUseCase

logger = logging.getLogger(__name__)


async def _run_lock_expiry_loop() -> None:
    interval = int(os.getenv("LOCK_EXPIRY_INTERVAL_SECONDS", "60"))
    while True:
        await asyncio.sleep(interval)
        use_case = ExpireSessionLocksUseCase(
            session_repository=get_session_repository(get_client())
        )
        expired_count = use_case.execute()
        if expired_count > 0:
            logger.info("locks_expired", extra={"count": expired_count})


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_run_lock_expiry_loop())
    yield
    task.cancel()


app = FastAPI(
    title="AgendaPro API",
    description="API de agendamento inteligente para professores.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(professors.router)
app.include_router(sessions.router)
app.include_router(appointments.router)
