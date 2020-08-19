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
        Public_Map = self.passMap()
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
        static_crime_path = staticfiles_storage.path('mapPage/csv/crime.csv')
        static_cctv_path = staticfiles_storage.path('mapPage/csv/cctv.csv')
        a = pd.read_csv(static_crime_path, thousands=',', encoding='euc-kr')
        b = pd.read_csv(static_cctv_path, thousands=',', encoding='euc-kr')
        a.head()
        b.head()
        
        #csv에서 지역을 받아 리스트로 넣어줌
        region = []
        for value in a:
            region.append(value)
        #
        del region[0:1]
        #print(region)

        x = [] #네이버 api에서 받은 위도
        y = [] #네이버 api에서 받은 경도
        z = [] #네이버 api에서 받은 지역이름
        cc = [] #cctv 위도
        tv = [] #cctv 경도

        #naver map api info
        for value in region:
            temp_map = self.search_map(value)
            temp_map = json.loads(temp_map)
            temp_map = temp_map['addresses'][0]
            x.append(float(temp_map['x']))
            y.append(float(temp_map['y']))
            z.append(temp_map['roadAddress'])

        # print(x) 
        m = folium .Map(
            location=(37.4729081, 127.039306),
            tiles='cartodbpositron',
            zoom_start=8
        )

        #정보 부분 출력
        fg_1 = folium.FeatureGroup(name='CCTV Location').add_to(m)
        fg_2 = folium.FeatureGroup(name='Crime List').add_to(m) 

        #지역별 범죄현황
        #               16개
        for i in range(len(x)):
            classes = ('table table-striped table-hover' 'taalbe-condensed table-responsive')

            popup = a.iloc[[0, 1, 2, 3, 4, 5, 6, 7], [0, i+1]].to_html(classes=classes)

            folium.Marker(
                [y[i],x[i]],
                popup=popup,
                icon=folium.Icon(color='blue')
            ).add_to(fg_1)

        #cctv append
        for i in range(373):
            cc.append(b.iloc[i, 2]) #위도
            tv.append(b.iloc[i, 3]) #경도


        radi = 30 #반경
        rotating_degree = 5 #회전각도 5개
        ar = 0 #비율, 교차하지 않은 경우의 값
        r = 50 #장소의 원의 반지름
        R = 10 #유저의 원의 반지름

        #cctv input
        for i in range(373):
            # c = 각 cctv의 좌표
            c = cc[i],tv[i] #36.94273371 / 126.780918
            #사용자 입력 주소 (위,경도 변환된값)
            R2_p = (37.459485, 126.905046)
            d = self.distance(c, R2_p)
            #d = math.floor(d)
            # for i in range(int(d)):
            #     if i < 10:
            #         print(i) 

            offsets = self.calc_offsets(radi, c[1])
            coordinates = [self.coordinate_after_rotation(c, e, offsets) for e in range(0, 360+1, rotating_degree)]
            # b = 각 cctv의 폴리곤화
            b = []
            for i in coordinates:
                b.append(i)

            folium.Marker(
                c,
                icon = folium.Icon(color='red'), #icon='C:/Users/His hacker/Desktop/gitlab/SK-Infosec/tens/images.png'
                popup = c
            ).add_to(fg_2)
            # 각 cctv의 폴리곤 원형화
            folium.Polygon(locations=b, fill=True, color='red', tooltip='Polygon').add_to(fg_2)

        folium.LayerControl(collapsed=False).add_to(m)
        m = m._repr_html_()
        return m