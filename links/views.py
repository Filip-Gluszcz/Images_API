from django.http import HttpResponseRedirect, HttpResponse
from .models import ExpiringLink
from django.utils import timezone

def expiring_link(request, code):
    '''
    Expiring link view. View will remove the link if it has expired.
    '''
    try:
        link = ExpiringLink.objects.get(code=code)
    except ExpiringLink.DoesNotExist:
        link = None

    if request.method == 'GET':
        if link:
            if link.expiration_date > timezone.now():
                return HttpResponseRedirect(link.image.image.url)
            else:
                link.delete()
                return HttpResponse('Expired link')
        else:
            return HttpResponse('Expired link')

