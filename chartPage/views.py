from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.

# Welcome and Search Page
class chartview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        context = {
            'user': request.user.username,
            'default': True,
        }
        return render(request, 'chartPage/chart.html', context)