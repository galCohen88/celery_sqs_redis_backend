from distutils.core import setup

setup(
    name='celery_sqs_redis_backend',
    version='0.1',
    packages=['svc'],
    install_requires=['Flask==1.1.1', 'celery[sqs]', 'kombu', 'redis==4.4.4', 'boto3'],
    long_description=open('README.md').read(),
)
