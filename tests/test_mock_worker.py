import asyncio
import pytest
from datetime import datetime, timezone
from app.db.session import AsyncSessionLocal
from app.models.task import Task, TaskStatus

@pytest.mark.asyncio
async def test_simulated_task_processing():
    async with AsyncSessionLocal() as db:
        task = Task(
            title="Async Test",
            description="Simulate work",
            status=TaskStatus.NEW,
            created_at = datetime.now(timezone.utc)
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)

        task.status = TaskStatus.IN_PROGRESS
        await asyncio.sleep(1)
        task.status = TaskStatus.COMPLETED
        task.result = "Test complete"
        task.finished_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(task)

        assert task.status == TaskStatus.COMPLETED
        assert task.result == "Test complete"
