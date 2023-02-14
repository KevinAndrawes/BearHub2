from django.urls import path
from . import views
app_name='bear'
urlpatterns = [
path("" ,views.index, name = "index"),
path("kevin" , views.kevin,  name = "kevin"),
path('StudentPage',views.StudentPage,name="stupage")
]