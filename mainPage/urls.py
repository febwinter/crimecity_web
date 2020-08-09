from django.urls import path, include
from mainPage.views import loginView
from . import views

urlpatterns = [
    path('', loginView.as_view(), name='login'),
]
