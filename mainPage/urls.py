from django.urls import path, include
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.userLoginView.as_view(), name='login'),
    path('signUp/', views.userRegister.as_view(), name='signUp'),
    path('complete/', views.registComplete.as_view(), name='complete')
]
