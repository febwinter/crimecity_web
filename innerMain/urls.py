from django.urls import path
from . import views

app_name = 'innerMain'

urlpatterns = [
    path('', views.mainview.as_view(), name='main'),
    path('test/', views.testView.as_view(), name='test')
]
