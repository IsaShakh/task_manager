from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List
from app.schemas.task import TaskCreate, TaskRead, TaskStatus
from app.models.task import Task, TaskStatus as TaskStatusDB
from app.db.session import get_db

router = APIRouter()

from app.workers.producer import publish_task

@router.post("/", response_model=TaskRead)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = Task(**task_in.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)

    publish_task(task.id)

    return task


@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    status: TaskStatus = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/{task_id}/status")
async def get_task_status(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task.status).where(Task.id == task_id))
    status = result.scalar_one_or_none()
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": status}

@router.delete("/{task_id}", response_model=TaskRead)
async def cancel_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status in [TaskStatusDB.COMPLETED, TaskStatusDB.CANCELLED]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed or cancelled task")
    task.status = TaskStatusDB.CANCELLED
    await db.commit()
    await db.refresh(task)
    return task
