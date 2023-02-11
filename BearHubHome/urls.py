from django.urls import path
from . import views

urlpatterns = [
path("" ,views.index, name = "index"),
path("kevin" , views.kevin,  name = "kevin"),
path("<str:name>",views.greet,name="greet"),

]