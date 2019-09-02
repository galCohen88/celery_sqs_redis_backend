from celery import Celery
from flask import Flask, request
from svc.tasks.tasks import long_task, dead_letter_q_task, task_retry

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/task')
def task():
    time = int(request.args.get('time', 0))
    block = bool(request.args.get('block', False))
    async_task = long_task.delay(time)
    if block:
        result = async_task.get()
        return 'waited %s blocking seconds' % str(result)
    return 'added new task to the Q'


@app.route('/dlq_task')
def dlq_task():
    dead_letter_q_task.delay()
    return 'added new dead letter task to the Q'


@app.route('/retry')
def retry():
    sleep = int(request.args.get('sleep', 0))
    task_retry.delay(sleep)
    return 'added new retry task'


@app.route('/non-existing')
def non_existing():
    celery_app_different_project = Celery()
    celery_app_different_project.conf.broker_url = 'sqs://asdf:asdf@alpine-sqs:9324/queue/default'
    celery_app_different_project.conf.result_backend = 'redis://redis:6379/0'
    celery_app_different_project.send_task('non_existing_task', kwargs={'url': 'https://google.com'}, queue='default')
    return 'added new non-existing task'


app.run(host="0.0.0.0", debug=True)
