from celery import shared_task
from .services import create_notification

@shared_task
def send_email_task(notification_id):
    # fetch Notification and send via email provider
    pass

@shared_task
def send_sms_task(notification_id):
    pass

@shared_task
def send_push_task(notification_id):
    pass
