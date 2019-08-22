# Dockerized celery project with SQS broker and Redis for results backend

#### Start

$ docker-compose up

$ docker-compose ps

![After up](svcs.png?raw=true "TFT screen")

#### Add job to SQS queue (from host)

$ curl http://localhost:5000/task

#### Task arguments

time - how much time will the task run

block - should API endpoint wait for task result to be returned 

$ curl http://localhost:5000/task?time=30&block=true

#### Visibility Timeout
The default Q is configured with 10 seconds  
Please note that if you pass time>10 duplications will occur

#### SQS control panel
to see SQS queues using web browser go to 

http://localhost:9325

![Messages in control panel](QQ.png?raw=true "TFT screen")

