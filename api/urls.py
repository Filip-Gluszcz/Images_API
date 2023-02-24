from django.urls import path, re_path
from . import views as api_views

urlpatterns = [
    path('images/', api_views.ImageList.as_view(), name='image_list'),
    path('images/upload/', api_views.ImageCreate.as_view(), name='image_upload'),
    path('images/<int:pk>/', api_views.ImageDetails.as_view(), name='image_details'),
    path('images/generate-expiring-link/', api_views.GenerateExpiringLink.as_view(), name='image_generate_expiring_link'),
]