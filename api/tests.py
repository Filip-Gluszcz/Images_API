from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from . import views as api_views
from images.models import Image, Thumbnail
from tiers.models import Tier, Account
from links.models import ExpiringLink
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


def temporary_image():
    from io import BytesIO
    from PIL import Image

    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


class ApiUrlsTests(SimpleTestCase):

    def test_image_list_url_is_resolved(self):
        url = reverse('image_list')
        self.assertEquals(resolve(url).func.view_class, api_views.ImageList)

    def test_image_upload_url_is_resolved(self):
        url = reverse('image_upload')
        self.assertEquals(resolve(url).func.view_class, api_views.ImageCreate)

    def test_image_details_url_is_resolved(self):
        url = reverse('image_details', args=(1,))
        self.assertEquals(resolve(url).func.view_class, api_views.ImageDetails)

    def test_image_generate_expiring_link_url_is_resolved(self):
        url = reverse('image_generate_expiring_link')
        self.assertEquals(resolve(url).func.view_class, api_views.GenerateExpiringLink)


class ImageApiViewsTests(APITestCase):
    
    def setUp(self):
        thumbnail = Thumbnail.objects.create(name='small', size=50)
        tier = Tier.objects.create(name='Basic', ori_img_link=True, expiring_link=True)
        tier.thumbnails.add(thumbnail)
        self.user = User.objects.create_user(username='admin', password='admin')
        acccount = Account.objects.create(user=self.user, tier=tier)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_authenticate(user=self.user, token=self.token)
        self.upload_url = reverse('image_upload')
        self.list_url = reverse('image_list')
        self.details_url = reverse('image_details', args=(1,))
        self.generate_url = reverse('image_generate_expiring_link')
        self.image = Image.objects.create(title='test', image=temporary_image(), user=self.user)
        
    def test_post_image_upload_authenticated(self):
        data = {
            'title': 'test',
            'image': temporary_image(),
        }
        response = self.client.post(self.upload_url, data, format='multipart')
        image = Image.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(image.user, self.user)

    def test_get_image_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_image_details_authenticated(self):
        response = self.client.get(self.details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_generate_expiring_link_authenticated(self):
        data = {
            'image': self.image.id,
            'expire_after': 300,
        }
        response = self.client.post(self.generate_url, data, format='json')
        links = ExpiringLink.objects.all()
        created_link = ExpiringLink.objects.last()
        url = reverse('expiring_link', args=[created_link.code])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(links.count(), 1)
        self.assertEqual(response.data['expiring_link'], f'http://testserver{url}')