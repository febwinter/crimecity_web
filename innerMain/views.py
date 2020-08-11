from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def mainView(request):
    return render(request, 'innerMain/main.html', request.get_username())


# class mainView(View):
#     def get(self, request):
#         return render(request, 'innerMain/main.html')