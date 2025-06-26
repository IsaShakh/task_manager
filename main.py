from fastapi import FastAPI
from app.api.v1.endpoints import tasks

app = FastAPI(title="Async Task Manager")

app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])