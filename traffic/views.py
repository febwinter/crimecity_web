from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
import requests
from bs4 import BeautifulSoup
from django.contrib.staticfiles.storage import staticfiles_storage

# Create your views here.
import folium
from folium.plugins import FastMarkerCluster
import pandas as pd
import json

# Welcome and Search Page
class trafficview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        private_map = self.passMap()
        context = {
            'user': request.user.username,
            'default': True,
            'map': private_map,
        }
        return render(request, 'traffic/traffic.html', context)

    def get_area(self, area_index):
        static_txt_path = staticfiles_storage.path('traffic/txt')
        IN_DIR = static_txt_path
        list_1 = [] 
        list_2 = [] 
        list_3 = [] 
        list_4 = [] 
        in_file = open(IN_DIR + "/congestion_coor_%02d.txt" % (area_index), 'r')
        step2 = in_file.readlines()

        for index_step in step2:
            index_step = index_step.replace("\n","")
            if index_step == "":
                continue
            index_step = index_step.strip()
            step = index_step
            tmpStep = step[0] 
            color = tmpStep[0]
            tmp_road = step[2:]
            tmp_road = tmp_road.split(',')
            tmp_road = [float (i) for i in tmp_road]
            lat_road = tmp_road[1::2]
            lon_road = tmp_road[0::2]
            n_range = len(lat_road)
            road = []
            for num in range(n_range):
                tmp_list =[]
                tmp_list.append(lat_road[num])
                tmp_list.append(lon_road[num])
                road.append(tmp_list)
            if color == '1':
                list_1.extend(road)
            elif color =='2':
                list_2.extend(road)
            elif color=='3':
                list_3.extend(road)
            else:
                list_4.extend(road)
        return (list_1, list_2, list_3, list_4)

    def passMap(self):
        static_geo_path = staticfiles_storage.path('traffic/json/skorea_municipalities_geo_simple.json')
        geo_str = json.load(open(static_geo_path, encoding='utf-8'))
        static_csv_path = staticfiles_storage.path('traffic/csv/Floating_Population_2005.csv')
        people_db = pd.read_csv(static_csv_path)
        people_db = people_db.rename(columns = {"일자":"date","시간(1시간단위)":"hour", "연령대(10세단위)":"age", "성별":"sex", "시":"seoul", "군구":"area", "유동인구수":"people_num"})
        df = pd.pivot_table(people_db,index ='area' ,columns ='hour',values='people_num')
        data_people = df[[21,22,23]]
        tmp_list = []
        for ri in range(25):
            tmp_list.append(data_people.iloc[ri][21]+data_people.iloc[ri][22]+data_people.iloc[ri][23])
        data_people['sum'] = tmp_list


        list_1 = []
        list_2 = [] 
        list_3 = [] 
        list_4 = [] 
        area = 16
        for ri in range(area):
            result = self.get_area(ri)
            list_1.extend(result[0])
            list_2.extend(result[1])
            list_3.extend(result[2])
            list_4.extend(result[3])

        satatic_predict_csv_path = staticfiles_storage.path('traffic/csv/Result.csv')
        visual_data = pd.read_csv(satatic_predict_csv_path)
        visual_data = visual_data.dropna()
        visual_list = []
        predict_data = visual_data[['long', 'lat']]


        for i in range(len(predict_data)):
            data = [predict_data.iloc[i]['lat'],predict_data.iloc[i]['long'] ]
            visual_list.append(data)
        map = folium.Map(location=[37.5502, 126.97], zoom_start=12,max_zoom=15, tiles='stamentoner')

        folium.Choropleth(geo_data=geo_str,
                    data=data_people['sum'],
                    columns=[df.index, data_people['sum']],
                    fill_color='YlGnBu',
                    key_on='feature.id').add_to(map)

        for ri in range(len(list_1)):
            folium.RegularPolygonMarker(location=list_1[ri], color='#ffc100',fill_color="#ffc100",number_of_sides=50, radius=1.5, rotation=1).add_to(map)
        for ri in range(len(list_2)):
            folium.RegularPolygonMarker(location=list_2[ri], color='#ff7400',fill_color='#ff7400',number_of_sides=50, radius=1.5, rotation=1).add_to(map)
        for ri in range(len(list_3)):
            folium.RegularPolygonMarker(location=list_3[ri], color='#ff4d00',fill_color='#ff4d00', number_of_sides=50, radius=1.5, rotation=1).add_to(map)
        for ri in range(len(list_4)):
            folium.RegularPolygonMarker(location=list_4[ri], color='#ff0000',fill_color='#ff0000', number_of_sides=50, radius=1.5, rotation=1).add_to(map)

        for rn in range(len(visual_list)):
            static_alert_path = staticfiles_storage.path('traffic/img/alert.png')
            icon = folium.features.CustomIcon(static_alert_path, icon_size = (26, 26))
            folium.Marker(
                location =visual_list[rn], 
                popup="prediction of crime", 
                icon = icon
            ).add_to(map)

        return map._repr_html_()