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
import gpxpy
# Create your views here.

# Welcome and Search Page
class mapview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        
        context = {
            'user': request.user.username,
            'default': True,
            # 'map' : Public_Map
        }
        return render(request, 'mapPage/map.html', context)

    def post(self, request):
        where_u_r = request.POST.get('search')
        Public_Map = self.passMap(where_u_r)
        context = {
            'user': request.user.username,
            'default': False,
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
    # def theta(self, R, r, d):
    #     return 2 * math.acos((pow(d, 2) + pow(R, 2) - pow(r, 2)) / (2 * d * R))
    # # 원점과 거리를 이용한 교차면적 계산
    # def intersection_area(self, R, r, d):
    #     t1 = self.theta(R, r, d)
    #     t2 = self.theta(r, R, d)
    #     return (pow(R, 2) * (t1 - math.sin(t1)) + pow(r, 2) * (t2 - math.sin(t2))) / 2

    def distance(self, R1, R2):
        #R1 = 136.9122221, 35.1299227
        #R2 = 136.9116187, 35.1295955
        lat1 = R1[0] 
        lon1 = R1[1]
        lat2 = R2[0]
        lon2 = R2[1]
        #return 110.25 * math.sqrt(pow(lat1 - lat2, 2) + pow((lon1 - lon2) * math.cos(math.radians(lat2)), 2))
        return gpxpy.geo.haversine_distance(lat1, lon1, lat2, lon2)/1000

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

    def passMap(self, where_u_r):
        static_crime_path = staticfiles_storage.path('mapPage/csv/crime.csv')
        static_cctv_path = staticfiles_storage.path('mapPage/csv/cctv.csv')
        static_police_path = staticfiles_storage.path('mapPage/csv/police.csv')
        a = pd.read_csv(static_crime_path, thousands=',', encoding='utf-8')
        b = pd.read_csv(static_cctv_path, thousands=',', encoding='utf-8')
        police = pd.read_csv(static_police_path, thousands=',',encoding='utf-8') 
        a.head()
        b.head()
        police.head()
        
        #사용자 입력값
        temp_user = self.search_map(where_u_r)
        temp_user = json.loads(temp_user)
        temp_user = temp_user['addresses'][0]
        print(temp_user)
        R2_p = (float(temp_user['y']),float(temp_user['x']))
        print(R2_p)


        #csv에서 지역을 받아 리스트로 넣어줌
        region = []
        for value in a:
            region.append(value)
        #
        del region[0:1]

        x = [] #네이버 api에서 받은 위도
        y = [] #네이버 api에서 받은 경도
        z = [] #네이버 api에서 받은 지역이름
        cc = [] #cctv 위도
        tv = [] #cctv 경도
        lst = []
        lst2 = []

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
            location= (R2_p),
            tiles='cartodbpositron',
            zoom_start=16
        )

        #정보 부분 출력
        fg_1 = folium.FeatureGroup(name='CCTV Location').add_to(m)
        fg_2 = folium.FeatureGroup(name='Crime List').add_to(m) 
        fg_3 = folium.FeatureGroup(name='Police Office').add_to(m) 
        fg_4 = folium.FeatureGroup(name='Distance to Police Office').add_to(m) 

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
        radi_user = 15 #유저반경
        rotating_degree = 45 #회전각도 5개
        ar = 0 #비율, 교차하지 않은 경우의 값
        r = 50 #장소의 원의 반지름
        R = 30 #유저의 원의 반지름

        #cctv input
        for i in range(373):
            # c = 각 cctv의 좌표
            c = cc[i],tv[i] #36.94273371 / 126.780918
            d = self.distance(c, (R2_p))
            d = d * 100
            tmp_array = [cc[i], tv[i], d]
            lst.append(tmp_array)
            offsets = self.calc_offsets(radi, c[1])
            coordinates = [self.coordinate_after_rotation(c, e, offsets) for e in range(0, 360+1, rotating_degree)]
            # b = 각 cctv의 폴리곤화
            b = []
            for i in coordinates:
                b.append(i)
            static_cctv_img = staticfiles_storage.path('mapPage/image/cctv.png')
            icon1 = folium.features.CustomIcon(static_cctv_img, icon_size=(17, 17))
            folium.Marker(
                c,
                icon = icon1,
                popup = c
            ).add_to(fg_2)

            folium.Circle(
                location = c,
                radius = 25,
                fill = True,
                color = 'red',
                tooltip = 'Polygon'
            ).add_to(fg_2)

        static_user_img = staticfiles_storage.path('mapPage/image/user.png')
        icon = folium.features.CustomIcon(static_user_img, icon_size=(15, 15)),
        folium.Marker(
            (R2_p),
            icon = folium.features.CustomIcon(static_user_img, icon_size=(15, 15)),
            popup = (R2_p)
        ).add_to(fg_2)

        folium.Circle(
            location = (R2_p),
            radius = 25,
            fill = True,
            popup = (R2_p)
        ).add_to(fg_2)

        crros_over = min(lst, key=lambda item: item[2])

        print(crros_over)
        R1_p = (crros_over[0], crros_over[1])
        pulse = (crros_over[2])

        #현재 위치 기준으로 반경내 이탈한지 체크
        if pulse < 5 :
            print("cctv 반경 내에 위치합니다.")
            #return # a = "cctv 반경 내에 위치합니다."
        else :
            print("cctv 반경에서 벗어났습니다.")
            #return # a = "cctv 반경에서 벗어났습니다."
        #return # a

        # 첫번째 = cctv안에 유저 전체가 들어감 print(36%) <= 고정값
        # 세번째 = cctv안에 유저가 일부 들어감 print(1~35%) <= 거리기반값
        # if pulse + R <= r : # 장소의 원안에 유저의 원이 존재할 경우
        #     ar = (math.pi * pow(R, 2)) / (math.pi * pow(r, 2)) 
        #     print("첫번째") 
        # elif pulse + r <= R : #유저의 원안에 장소의 원이 존재할 경우
        #     ar = 1.0
        #     print("두번째")
        # elif pulse < R + r : #두 원이 겹쳐지지 않은 경우 + 부분적으로 겹쳐진경우 MAX =36 ,Min = 1 
        #     ar = self.intersection_area(R, r, d) / (math.pi * pow(r, 2))
        #     print("세번째")
        # else :
        #     print("에러")


        police_we = []
        police_gang = []
        for i in range(2264):
            police_we.append(police.iloc[i, 4]) #위도
            police_gang.append(police.iloc[i, 3]) #경도

        for i in range(2264):
            police_loc = (police_we[i],police_gang[i])
            police_d = self.distance(police_loc, (R2_p))
            police_d = police_d * 1000
            police_array = [police_we[i], police_gang[i], police_d]
            lst2.append(police_array)

            static_police_img = staticfiles_storage.path('mapPage/image/police.png')
            icon2 = folium.features.CustomIcon(
                static_police_img, 
                icon_size=(20, 20)
                )
            folium.Marker(
                police_loc,
                icon=icon2,
                popup = police_loc
            ).add_to(fg_3)


        for i in lst2:
            if i[2] < 1000:
                test_lat_lon = i[0:2]
                locations = (R2_p)
                data=[]
                data.append(locations)
                data.append(test_lat_lon)
                print(data)
                popup3 = str(round(i[2])) + 'm'
                folium.plugins.PolyLineOffset(
                    data,
                    popup = popup3,
                    color = "black", 
                    opacity=1,
                    offset=-5,
                    dash_array = "5,10"
                ).add_to(fg_4)


        folium.LayerControl(collapsed=False).add_to(m)
        return m._repr_html_()