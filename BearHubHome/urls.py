from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='bear'
urlpatterns = [
path("",views.index,name="index"),
path("LogIn" ,views.LogIn, name = "LogIn"),
path("kevin" , views.kevin,  name = "kevin"),
path('StudentPage/<int:user_id>/',views.StudentPage,name="stupage"),
path('SignUp',views.SignUp,name="signUp")
]