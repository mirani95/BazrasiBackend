from celery import shared_task
from apps.product.models import SaleUnit


@shared_task(bind=True)
def task_func(self):
    print("Task Is Running.....")
    return 'Done'
