from django.urls import path, include
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.userLoginView.as_view(), name='login'),
    path('register/', views.userRegister.as_view(), name='register')
]
