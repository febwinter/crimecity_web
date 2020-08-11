from django.urls import path
from innerMain.views import mainView
from django.contrib.auth import views as auth_views

app_name = 'innerMain'

urlpatterns = [
    path('', mainView, name='main'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mainpage/login'), name='logout'),
]
