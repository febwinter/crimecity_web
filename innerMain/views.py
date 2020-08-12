from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.

class mainview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        # print(request.user.username)
        context = {
            'user' : request.user.username
        }
        return render(request, 'innerMain/main.html', context)