from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create your views here.

# Welcome and Search Page
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

    # def get(self, request):
    #     return render(request, 'innerMain/sample.html')

    # def crawling_news(self, request):
    def get(self, request):
        search_keyword = '범죄'
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search_keyword}'

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        news_titles = soup.select('.news .type01 li dt a[title]')
        news_links = soup.select('.news .type01 li dt a[href]')
        news_info = soup.findAll("span",{"class":"_sp_each_source"})

        title_data = []
        for title in news_titles:
            title_data.append(title.get_text())

        link_list = []
        for title in news_links:
            link = title['href']
            link_list.append(link)

        info_list = []
        for title in news_info:
            info_list.append(title.get_text())

        link_data = dict(zip(title_data, link_list)) # 제목  : 링크
        paper_data = dict(zip(title_data, info_list)) # 제목 : 신문사
        context = {
            'title' : title_data,
            'link' : link_list,
            'paper' : info_list,
            'linkData' : link_data
        }
        print(title_data)
        return render(request, 'innerMain/sample.html', context)
        # data = {
        #     'title' : title_list,
        #     'info' : info_list,
        #     'link' : link_list
        # }
        # # print(data)
        # df = pd.DataFrame(data, columns=["title", "info", "link"])
        # news_data = df
        # news_show_data = news_data[["title", "info", "link"]]
        # news_show_data

        # news_html = news_show_data.to_html(index=False, justify='center')
        # # print(news_html)

        # """## link는 a로 넣고, table은 2개로만"""

        # news_data[["link"]]



        return render(request, 'innerMain/sample.html')