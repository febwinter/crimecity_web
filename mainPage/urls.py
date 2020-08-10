from django.urls import path, include
from django.contrib.auth import views as auth_views
from mainPage.views import loginView
from . import views

app_name = 'mainPage'

urlpatterns = [
    # path('', loginView.as_view(), name='login'),
    path('', auth_views.LoginView.as_view(template_name='mainPage/login.html'), name='login')
]
