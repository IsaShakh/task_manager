import pika
import json
from app.core.config import settings

def publish_task(task_id: int):
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue='tasks')

    message = json.dumps({"task_id": task_id})
    channel.basic_publish(exchange='', routing_key='tasks', body=message)

    connection.close()
