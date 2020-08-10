from django.urls import path
from prediction.views import mainView

app_name = 'prediction'

urlpatterns = [
    path('', mainView, name='main'),
]