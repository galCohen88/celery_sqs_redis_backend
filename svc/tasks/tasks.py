import time
from celery import Celery
from kombu import Queue

app = Celery()

# app.conf.broker_url = 'sqs://localhost:9324/queue'
# app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.broker_url = 'sqs://asdf:asdf@alpine-sqs:9324/queue'
app.conf.result_backend = 'redis://redis:6379/0'

# visibility timeout is set to 10 seconds for default Q
app.conf.task_queues = (
    Queue('default', routing_key='default'),
)

app.conf.task_routes = ([
    ('svc.tasks.tasks.long_task', {'queue': 'default'}),
],)


# without acks_late flag the message will be acked
# when message is consumed!
@app.task(acks_late=True)
def long_task(task_time_secs):
    for i in range(0, task_time_secs):
        time.sleep(1)
        print(str(i))
    return task_time_secs
