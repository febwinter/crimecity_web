from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.

class mainview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        context = {
            'user' : request.user.username
        }
        return render(request, 'innerMain/welcome_search.html', context)

    def post(self,request):
        context = {
            'user' : request.user.username
        }
        return render(request, 'innerMain/search_result.html', context)


# Test for Django HTML
class testView(View):

    def get(self, request):
        return render(request, 'innerMain/sample.html')

