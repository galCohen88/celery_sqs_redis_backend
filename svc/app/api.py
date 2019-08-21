from flask import Flask
from svc.tasks.tasks import long_task

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/task')
def task():
    long_task.delay()
    return 'added new task to the Q'


app.run(host="0.0.0.0", debug=True)
