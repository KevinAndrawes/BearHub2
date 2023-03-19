from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='bear'
urlpatterns = [
path("",views.index,name="index"),
path("LogIn" ,views.LogIn, name = "LogIn"),
path('StudentPage/<int:user_id>/',views.StudentPage,name="stupage"),
path('SignUp',views.SignUp,name="signUp"),
path('AdminLogIn',views.adminLogIn,name="adminLogIn"),
path('AdminPage/<int:user_id>/',views.AdminPage,name="adpage"),
path('UpdateValues', views.Update , name="updater"),
path('NewEvent', views.NewEvent , name="NewEvent"),
path('request_event/', views.requestEvent, name='requestEvent'),
path('accept_request', views.accept_request, name='accept_request'),
path('report',views.report,name="report"),
path('claim_reward',views.claim_reward,name='claim_reward'),
path('help',views.help,name='help'),
path('events', views.events, name='events'),
path('checkReward',views.checkReward,name='checkReward'),
]