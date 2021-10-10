from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.index, name="home"),
    path("cc1",views.cc1, name="cc1"),
    path("qz<int:quiz_id>",views.qz, name="qz"),
    path("qz<int:quiz_id>/check",views.check, name="check"),
    path("ques<int:question_id>",views.ques, name="ques"),
    path("ques<int:question_id>/check",views.qcheck, name="qcheck"),
    path("start<int:quiz_id>",views.start, name="start"),
    path("login", views.login_view,name="login"),
    path("logout", views.logout_view,name="logout")
]