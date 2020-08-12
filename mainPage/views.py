from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

# Create your views here.
class userLoginView(LoginView):
    template_name = 'mainPage/login.html'

class userRegister(CreateView):
    template_name = 'mainPage/signUp.html'
    form_class = UserCreationForm
    success_url = '/login/complete/'

class registComplete(View):
    def get(self, request):
        return render(request, 'mainPage/complete.html')


