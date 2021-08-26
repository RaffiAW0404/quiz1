from django.urls import path 
from . import views 

urlpatterns = [
    path("index",views.index, name="index"),
    path("cc1",views.cc1, name="cc1"),
    path("qz1001",views.qz1001, name="qz1001")
]