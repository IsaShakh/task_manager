import pika
import json
import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.task import Task, TaskStatus

async def process_task(task_id: int):
    async with AsyncSessionLocal() as db:
        task = await db.get(Task, task_id)
        if not task:
            return

        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            task.status = TaskStatus.COMPLETED
            task.finished_at = datetime.now(timezone.utc)
            task.result = f"Task {task.id} completed successfully"
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
        finally:
            await db.commit()

def callback(ch, method, properties, body):
    data = json.loads(body)
    task_id = data.get("task_id")
    asyncio.run(process_task(task_id))

def main():
    connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq/"))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
