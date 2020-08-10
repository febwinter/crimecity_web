from django.urls import path
from dataGraph.views import mainView

app_name = 'dataGraph'

urlpatterns = [
    path('', mainView, name='main'),
]