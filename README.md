# celery_sqs_redis_backend

Dockerized celery project with SQS broker and Redis for results backend

####Start

docker-compose up
![After up](svcs.png?raw=true "TFT screen")

#### Add job to SQS queue (from host)

curl http://localhost:5000/task

#### SQS control panel
to see SQS queues using web browser go to 

http://localhost:9325

![Messages in control panel](Q.png?raw=true "TFT screen")

