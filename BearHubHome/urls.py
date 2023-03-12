from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='bear'
urlpatterns = [
path("",views.index,name="index"),
path("LogIn" ,views.LogIn, name = "LogIn"),
path("kevin" , views.kevin,  name = "kevin"),
path('StudentPage/<int:user_id>/',views.StudentPage,name="stupage"),
path('SignUp',views.SignUp,name="signUp"),
path('AdminLogIn',views.adminLogIn,name="adminLogIn"),
path('AdminPage/<int:user_id>/',views.AdminPage,name="adpage"),
path('UpdateValues', views.Update , name="updater"),
path('NewEvent', views.NewEvent , name="NewEvent"),
path('request_event/', views.requestEvent, name='requestEvent'),

]