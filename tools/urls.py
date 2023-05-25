from django.urls import path 

from . import views 

app_name = 'tools'
urlpatterns = [
    path("", views.index, name="index"),
    path("mx_converter", views.mx_converter, name="mx_converter"),
]