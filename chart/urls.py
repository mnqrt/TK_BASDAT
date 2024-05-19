from django.urls import path
from chart.views import chart_list, chart_detail

app_name = 'chart'

urlpatterns = [
    path('chart-list/', chart_list, name='list_chart'),
    path('chart-detail/', chart_detail, name='detail_chart'),
]