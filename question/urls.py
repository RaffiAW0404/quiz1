from django.urls import path 
from . import views 

urlpatterns = [
    path("index",views.index, name="home"),
    path("cc1",views.cc1, name="cc1"),
    path("qz<int:quiz_id>",views.qz, name="qz")
]