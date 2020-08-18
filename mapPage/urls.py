from django.urls import path
from . import views

app_name = 'mapPage'

urlpatterns = [
    path('crime_cctv/', views.mainview.as_view(), name='crime_cctv')
]
