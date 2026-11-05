from django.urls import path
from pipeline import views

urlpatterns = [
    path('api/upload/', views.upload_view, name='upload'),
    path('api/stats/', views.stats_view, name='stats'),
    path('api/config/', views.config_view, name='config'),
    path('api/preview/', views.preview_view, name='preview'),
]
