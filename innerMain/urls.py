from django.urls import path
from innerMain.views import mainView

app_name = 'innerMain'

urlpatterns = [
    path('', mainView, name='main'),
]
