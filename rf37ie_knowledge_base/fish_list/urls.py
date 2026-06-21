from django.urls import path
from . import views, api

app_name = 'fish_list'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('table/', views.fish_list, name='fish_list'),
    path('search/', views.fish_search, name='fish_search'),
    path('import-fishlog/', views.import_fishlog, name='import_fishlog'),
    path('fishlogs/', views.fishlog_data, name='fishlog_data'),
    path('bait-efficiency/', views.bait_efficiency, name='bait_efficiency'),

    # API Stuff

    path('api/fish-data/', api.get_fish_data, name='fish_data_api'),
    path('api/fishlog-data/', api.get_all_fishlogs, name='fishlog_data_api'),
    path('api/filter-options/', api.get_filter_options, name='filter_options_api'),
    path('api/all-options/', api.get_all_options, name='all_options_api'),
    path('api/bait-statistics/', api.get_bait_statistics, name='bait_statistics_api'),
    path('api/bait-efficiency/', api.find_average_bait_efficiency, name='bait_efficiency_api'),
    path('api/fish-list/', api.get_fish_list, name='fish_list_api'),
]