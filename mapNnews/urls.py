from django.urls import path
from mapNnews.views import mainView

app_name = 'mapNnews'

urlpatterns = [
    path('', mainView, name='mapNnews'),
]