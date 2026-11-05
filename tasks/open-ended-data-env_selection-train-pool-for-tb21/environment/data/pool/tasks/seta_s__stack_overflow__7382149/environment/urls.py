from django.contrib import admin
from django.urls import path
from taskboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health_check, name='health_check'),
]
