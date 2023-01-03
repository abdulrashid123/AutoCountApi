from celery import shared_task
from datetime import datetime


@shared_task(bind=True)
def test(self):
    for i in range(10):
        print(10)
    return "Done"