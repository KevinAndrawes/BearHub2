from django.shortcuts import render
import datetime
# Create your views here.
def index(request):
    return render(request,"bdays/birthday.html")

def birthday(request):
    today = datetime.date.today()
    d1 = today.strftime("%d/%m")
    print(d1)
    Time="No"
    print("hi")
    if(d1=="30/05"):
        Time= "Yes"
    return render(request,"bdays/birthday.html",{"value": Time})