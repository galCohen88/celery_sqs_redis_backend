from flask import Flask, request
from svc.tasks.tasks import long_task, dead_letter_q_task, task_retry

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/task')
def task():
    time = int(request.args.get('time'))
    block = bool(request.args.get('block'))
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
    sleep = int(request.args.get('sleep'))
    task_retry.delay(sleep)
    return 'added new retry task'


app.run(host="0.0.0.0", debug=True)
