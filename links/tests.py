from django.test import SimpleTestCase
from django.urls import resolve, reverse
from . import views

class LinkUrlsTests(SimpleTestCase):

    def test_expiring_link_url_is_resolved(self):
        url = reverse('expiring_link', args=('jclwjbelbefvpibv',))
        self.assertEquals(resolve(url).func, views.expiring_link)
