from django.urls import path
from . import views

app_name = 'noteBoard'

urlpatterns = [
    path('', views.boardview.as_view(), name='board')
]