from django.shortcuts import render
from django.views.generic import View
# from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseRedirect
# from .models import UserInfo

# Create your views here.
class loginView(View):
    def get(self, request):
        return render(request, 'mainPage/login.html')

    # def post(self, request):
    #     mail = request.POST.get('user_email')
    #     pw = request.POST.get('user_pw')
    #     msg = False
    #     infos = UserInfo.objects.all()  #Info 가 model, 별도의 DB에 저장된 내용을 불러온다
    #     for info in infos:
    #         if info.user_email == mail and info.user_password == pw:
    #             name = info.user_name
    #             # request.session.[]
    #             msg = True
        
        
    #     if msg == True:
    #         msg = 'Hello {} Login Success!'.format(name)
    #         context = {
    #             'msg' : msg,
    #         }
    #         return render(request, 'mainPage/main.html', context)
    #     else:
    #         msg = 'Incorrect Information'
    #         context = {
    #             'msg' : msg,
    #         }
    #         return render(request, 'mainPage/login.html', context)



        