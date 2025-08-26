from .models import Notification

def create_notification(user, title, body, channel="EMAIL"):
    n = Notification.objects.create(user=user, title=title, body=body, channel=channel)
    # integrate with email/sms/push providers here or call Celery tasks
    return n
