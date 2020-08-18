from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.staticfiles.storage import staticfiles_storage

# Map Create Modules
import urllib.request
import json
import pandas as pd
import folium
import folium.plugins
import math
import ssl
# Create your views here.

# Welcome and Search Page
class mapview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        Public_Map = 0
        self.passMap()
        context = {
            'user': request.user.username,
            'default': True,
            'map' : Public_Map
        }
        return render(request, 'mapPage/map.html', context)

    def calc_offsets(self, radi, lat):
        return (
        abs(360*math.asin(math.sin(radi/6271/2/2000)/math.cos(lat*math.pi/180))/math.pi),
        180*radi/6371/1000/math.pi
        )

    def coordinate_after_rotation(self, c, degree, offsets):
        return (
            c[0]+math.cos(math.pi/180*degree)*offsets[0],
            c[1]+math.sin(math.pi/180*degree)*offsets[1]
        )
    # 원점과 거리를 이용한 교차면적 계산
    def intersection_area(self, R, r, d):
        t1 = 2 * math.acos((pow(d, 2) + pow(R, 2) - pow(r, 2)) / (2 * d * R))
        t2 = 2 * math.acos((pow(d, 2) + pow(r, 2) - pow(R, 2)) / (2 * d * r))
        return (pow(R, 2) * (t1 - math.sin(t1)) + pow(r, 2) * (t2 - math.sin(t2))) / 2

    def distance(self, R1, R2):
        #R1 = 136.9122221, 35.1299227
        #R2 = 136.9116187, 35.1295955
        lat1 = R1[0] 
        lon1 = R1[1]
        lat2 = R2[0]
        lon2 = R2[1]
        return 110.25 * math.sqrt(pow(lat1 - lat2, 2) + pow((lon1 - lon2) * math.cos(math.radians(lat2)), 2))

    #naver maps api return module
    def search_map(self, search_text):
        client_id = '2o352tcqq0'
        client_secret = 'ZlXWXWm2BsZRkYOcv1ZiXm6vUEqCiQ042yABG7JR'
        encText = urllib.parse.quote(search_text)
        url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='+encText
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib.request.Request(url)
        request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
        request.add_header('X-NCP-APIGW-API-KEY', client_secret)
        response = urllib.request.urlopen(request)
        #server info get
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            #print(response_body.decode('utf-8'))
            return response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)

    def passMap(self):
        static_crime_path = staticfiles_storage.url('csv/crime.csv')
        static_cctv_path = staticfiles_storage.url('csv/cctv.csv')
        a = pd.read_csv(static_crime_path, thousands=',', encoding='euc-kr')
        b = pd.read_csv(static_cctv_path, thousands=',', encoding='euc-kr')
        a.head()
        b.head()
        print(static_cctv_path," : ", static_crime_path)
