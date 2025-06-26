import pytest
from app.schemas.task import TaskPriority

@pytest.mark.asyncio
async def test_create_task(async_client):
    payload = {
        "title": "Test Task",
        "description": "Test Desc",
        "priority": TaskPriority.MEDIUM.value
    }
    response = await async_client.post("/api/v1/tasks/", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]

@pytest.mark.asyncio
async def test_get_task_by_id(async_client):
    create = await async_client.post("/api/v1/tasks/", json={
        "title": "Test ID", "priority": "LOW"
    })
    task_id = create.json()["id"]
    response = await async_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

@pytest.mark.asyncio
async def test_cancel_task(async_client):
    create = await async_client.post("/api/v1/tasks/", json={
        "title": "To Cancel", "priority": "LOW"
    })
    task_id = create.json()["id"]
    cancel = await async_client.delete(f"/api/v1/tasks/{task_id}")
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "CANCELLED"
