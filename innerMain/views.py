from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import NewsData
import requests
from bs4 import BeautifulSoup

# Create your views here.

# Welcome and Search Page
class mainview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        context = {
            'user': request.user.username,
            'default': True,
        }
        return render(request, 'innerMain/welcome_search.html', context)

    def get_link(self, p_url):
        html = requests.get(p_url).text.strip()
        soup = BeautifulSoup(html, 'html5lib')
        r_news_link = soup.select('.coll_cont ul li a.f_link_b')
        return r_news_link

    def post(self, request):
        keyword = request.POST.get('search')
        title_list = []
        link_list = []
        img_list = []
        to_check = []
        text_list = []

        url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page={0}&q={1}'.format(1, keyword)
        news_link = self.get_link(url)

        for contents in news_link:
            link = contents.get('href')
            link_list.append(link)
            titles = contents.text
            title_list.append(titles)

        html = requests.get(url).text.strip() 
        soup = BeautifulSoup(html, 'html5lib')
        photos = soup.select("div.wrap_thumb div a img[src]")
        texts = soup.select("li > div.wrap_cont > div > p")

        for i in photos:
            img = i["src"]
            print(len(img))
            img_list.append(img)

        for i in texts:
            text = i.get_text()
            text_list.append(text)

        for i in range(10):
            img = soup.select("#news_img_{0} > div > a > img[src]".format(i))
            to_check.append(img)

        for i, check in enumerate(to_check):
            if len(check) == 0:
                img_list.insert(i, "https://images.unsplash.com/photo-1560575193-c2c9e886aefe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80")

        item_num = len(title_list)
        item_list = []
        for i in range(item_num):
            item_list.append(NewsData(title_list[i], img_list[i],text_list[i], link_list[i])) # title, image, summary, link

        
        context = {
            'user' : request.user.username,
            'default' : False,
            'keyword' : keyword,
            'items' : item_list,
            'length' : item_num

        }
        return render(request, 'innerMain/welcome_search.html', context)




# Test for Django HTML
class testView(View):

    def get(self, request):
        search_keyword = '범죄'
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search_keyword}'

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        news_titles = soup.select('.news .type01 li dt a[title]')
        news_links = soup.select('.news .type01 li dt a[href]')
        news_info = soup.findAll("span", {"class":"_sp_each_source"})

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

        link_data = dict(zip(title_data, link_list))
        context = {
            'title' : title_data,
            'link' : link_list,
            'paper' : info_list,
            'linkData' : link_data
        }
        return render(request, 'innerMain/sample.html', context)
