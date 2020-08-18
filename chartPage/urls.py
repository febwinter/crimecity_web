from django.urls import path
from . import views

app_name = 'chartPage'

urlpatterns = [
    path('', views.chartview.as_view(), name='chart')
]
