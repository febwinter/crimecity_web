from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Region_Info
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd

class chartview(LoginRequiredMixin, View):

    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):

        regions = self.get_vis_data('chartPage/csv/rd_seoul.csv') # cirme number list
        regionsCircle = self.get_vis_data_cir('chartPage/csv/rd_seoul_planning.csv')
        context = {
            'user': request.user.username,
            'default': True,
            'regions': regions,
            'circle_data': regionsCircle,
        }
        return render(request, 'chartPage/chart.html', context)

    def get_vis_data(self, path):
        static_chart_data_path = staticfiles_storage.path(path)
        data = pd.read_csv(static_chart_data_path, thousands=',', encoding='utf-8')
        region_object_list = []
        rows = len(data)
        for row in range(rows):
            rData = data.loc[row].tolist()
            region_object_list.append(Region_Info(row, rData[0], rData[1:]))


        return region_object_list

    def get_vis_data_cir(self, path):
        static_chart_data_path = staticfiles_storage.path(path)
        data = pd.read_csv(static_chart_data_path, thousands=',', encoding='utf-8')
        data = data.drop(["총합계"],axis=1)
        region_object_list = []
        rows = len(data)
        for row in range(rows):
            rData = data.loc[row].tolist()
            total = sum(rData[1:])
            avData = [d/total * 100 for d in rData[1:]]
            region_object_list.append(Region_Info(row, rData[0], avData))


        return region_object_list