from flask import Flask, request
from svc.tasks.tasks import long_task

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/task')
def task():
    time = int(request.args.get('time'))
    long_task.delay(time)
    return 'added new task to the Q'


app.run(host="0.0.0.0", debug=True)
