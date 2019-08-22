import time
from celery import Celery
from kombu import Queue
from kombu.utils.url import quote

app = Celery()

# app.conf.broker_url = 'sqs://localhost:9324/queue'
# app.conf.result_backend = 'redis://localhost:6379/0'
# app.conf.broker_url = 'sqs://asdf:asdf@alpine-sqs:9324/queue'

aws_access_key = quote('')
aws_secret_key = quote('')

app.conf.broker_url = 'sqs://{aws_access_key}:{aws_secret_key}@sqs.us-east-1.amazonaws.com/160043208412/celery-test'.format(
    aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)
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
