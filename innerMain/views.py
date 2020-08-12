from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View

# Create your views here.

class mainview(View):

    @login_required
    def get(self, request):
        return render(request, 'innerMain/main.html')