import time
from celery import Celery


app = Celery()

# app.conf.broker_url = 'sqs://localhost:9324/queue'
# app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.broker_url = 'sqs://asdf:asdf@alpine-sqs:9324/queue'
app.conf.result_backend = 'redis://redis:6379/0'


@app.task(acks_late=True)
def long_task():
    count = 0
    while True:
        count += 1
        time.sleep(1)
        print(str(count))
