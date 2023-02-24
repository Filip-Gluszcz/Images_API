from celery import shared_task
from .models import ExpiringLink
from django.utils import timezone

@shared_task
def remove_expired_links():
    '''
    Interval task to remove expired links.
    '''
    if ExpiringLink.objects.filter(expiration_date__lte=timezone.now()).exists():
        expired_links = ExpiringLink.objects.filter(expiration_date__lte=timezone.now())
        expired_links_count = expired_links.count()
        expired_links.delete()
        return f'Removed {expired_links_count} expired links'
    else:
        return 'No links to remove'