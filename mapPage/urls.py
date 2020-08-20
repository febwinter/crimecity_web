from django.urls import path
from . import views

app_name = 'mapPage'

urlpatterns = [
    path('', views.mapview.as_view(), name='map')
]