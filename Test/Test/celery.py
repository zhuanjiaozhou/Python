from ast import arg
from cgi import test
from multiprocessing.reduction import dump
import os
from unittest import TestCase

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
import django
django.setup()

app = Celery('Test')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


from celery.schedules import crontab
from Test.tasks import add

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'Test.tasks.add',
        'schedule': 10.0,
        'args': (16, 4)
    },
}

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

# ## 定时任务
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule

## 先创建定时策略
schedule, create = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
## 再创建任务
task = PeriodicTask.objects.get_or_create(interval=schedule, name='say welcome 2023', task = 'Test.celery.test', args=json.dumps(['welcome 2023']),)

@app.task
def test(arg):
    print(arg)

app.conf.timezone = "Asia/Shanghai"