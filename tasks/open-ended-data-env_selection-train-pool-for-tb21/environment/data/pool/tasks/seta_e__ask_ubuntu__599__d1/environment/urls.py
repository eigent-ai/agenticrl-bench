from django.urls import path
from myproject.myapp import views

urlpatterns = [
    path("version/", views.version_view),
]
