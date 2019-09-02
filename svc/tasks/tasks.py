import time
from celery import Celery
from celery.worker.consumer import Consumer
from kombu import Queue

app = Celery()


def on_unknown_task(self, body, message, exc):
    task_name = message.headers.get('task')
    task_id = message.headers.get('id')
    print(f'[on_unknown_task] Ignoring and acknowledging message for unknown task. Task name: {task_name}, Task id: {task_id}')
    message.ack()


Consumer.on_unknown_task = on_unknown_task

# app.conf.broker_url = 'sqs://localhost:9324/queue'
# app.conf.result_backend = 'redis://localhost:6379/0'


app.conf.broker_url = 'sqs://asdf:asdf@alpine-sqs:9324/queue/default'
app.conf.result_backend = 'redis://redis:6379/0'


app.conf.max_retries = 3

# visibility timeout is set to 10 seconds for default Q
app.conf.task_queues = (
    Queue('default', routing_key='default'),
)

app.conf.task_routes = ([
    ('svc.tasks.tasks.long_task', {'queue': 'default'}),
    ('svc.tasks.tasks.dead_letter_q_task', {'queue': 'default'}),
    ('svc.tasks.tasks.task_retry', {'queue': 'default'}),
],)


# without acks_late flag the message will be acked
# when message is consumed!
@app.task(acks_late=True)
def long_task(task_time_secs):
    for i in range(0, task_time_secs):
        time.sleep(1)
        print(str(i))
    return task_time_secs


@app.task(acks_late=True, acks_on_failure_or_timeout=False)
def dead_letter_q_task():
    return 1/0


@app.task(bind=True, acks_late=True)
def task_retry(self, secs):
    print("going to sleep for %s" % str(secs))
    time.sleep(secs)
    self.retry()
