from django.urls import path
from . import views

app_name = 'fish_list'

urlpatterns = [
    path('', views.fish_list, name='fish_list'),
    path('search/', views.fish_search, name='fish_search'),
    path('api/fish-data/', views.get_fish_data, name='fish_data_api'),
    path('import-fishlog/', views.import_fishlog, name='import_fishlog'),
]