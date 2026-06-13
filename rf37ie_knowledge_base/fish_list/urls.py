from django.urls import path
from . import views

app_name = 'fish_list'

urlpatterns = [
    path('', views.fish_list, name='fish_list'),
    path('search/', views.fish_search, name='fish_search'),
    path('import-fishlog/', views.import_fishlog, name='import_fishlog'),
    path('fishlogs/', views.fishlog_data, name='fishlog_data'),
    path('api/fish-data/', views.get_fish_data, name='fish_data_api'),
    path('api/fishlog-data/', views.get_all_fishlogs, name='fishlog_data_api'),
    path('api/filter-options/', views.get_filter_options, name='filter_options_api'),
    path('api/all-options/', views.get_all_options, name='all_options_api'),
    path('api/bait-statistics/', views.get_bait_statistics, name='bait_statistics_api'),
]