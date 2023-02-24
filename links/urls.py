from django.urls import path
from . import views

urlpatterns = [
    path('temp/<str:code>/', views.expiring_link, name='expiring_link'),
]