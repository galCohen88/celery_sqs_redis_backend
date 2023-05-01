from distutils.core import setup

setup(
    name='celery_sqs_redis_backend',
    version='0.1',
    packages=['svc'],
    install_requires=['Flask==2.3.2', 'celery[sqs]', 'kombu', 'redis==2.10.6', 'boto3'],
    long_description=open('README.md').read(),
)
