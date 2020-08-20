from django.urls import path
from . import views

app_name = 'traffic'

urlpatterns = [
    path('', views.trafficview.as_view(), name='traffic')
]