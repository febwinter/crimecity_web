from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import 
from django.views.generic import CreateView

# Create your views here.
class userLoginView(LoginView):
    template_name = 'mainPage/login.html'

class userRegister(CreateView):
    template_name = 'mainPage/register.html'
    form_class = UserCreationForm
    success_url = 'mainPage/login'

    def POST(request):
        form_class.save()
        username = form_class.cleaned_data.get('username')
        raw_password = form_class.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('home')

