from django.urls import path 
from . import views 

#these are the urls for my quiz app that define which functions in the 
#views.py are called when the page is directed to that url

urlpatterns = [
    path("",views.index, name="home"),
    path("cc1",views.cc1, name="cc1"),
    path("ques<int:question_id>",views.ques, name="ques"),
    path("ques<int:question_id>/check",views.qcheck, name="qcheck"),
    path("start<int:quiz_id>",views.start, name="start"),
    path("login", views.login_view,name="login"),
    path("logout", views.logout_view,name="logout"),
    path("signUp", views.signUp,name="signUp"),
    path("welcome",views.welcome_view,name="welcome"),
    path("change",views.change,name="change"),
    path("profile",views.profile,name="profile"),
    path("lead<int:quiz_id>",views.lead,name="lead"),
    path("ledas",views.leads,name="leads"),
    path("end",views.end,name="end"),
    path("feedback<int:question_id>",views.feedback,name="feedback"),
    path("create",views.create,name="create"),
    path("createq",views.createq,name="createq"),
    path("buildq",views.buildq,name="buildq")
]
#the use of the variable <int:question_id> in the url means that after the prefix 'ques' 
#a variable in integer type will be passed into the views.ques function allowing 
#for a single url for every question
#the same applies for the quiz_id variable