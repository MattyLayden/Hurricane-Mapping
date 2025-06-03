

from django.urls import path
from . import views

urlpatterns = [
    path('get_map_storm_by_name_year_modern/', views.get_map_storm_by_name_year_modern, name='get_storm_by_name_year'),
    path('get_map_storm_by_name_year_older/',views.get_map_storm_by_name_year_older, name='get_storm_by_name_year2' ),
    path('get_stormnames_from_year/', views.get_stormnames_from_year, name='get_stormnames_by_year'),
    path('get_heatmap_storms_by_year', views.get_heatmap_storms_by_year),
    path('get_predictions/', views.get_predictions_by_month, name='get_predictions_by_month')
]

