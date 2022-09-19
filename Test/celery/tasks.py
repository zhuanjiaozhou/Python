from celery import Celery

app = Celery('tasks', backend='redis://192.168.1.189', broker='redis://192.168.1.189')

@app.task
def add(x, y):
    return x + y