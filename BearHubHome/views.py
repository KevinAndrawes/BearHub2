from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

# Create your views here.
def index(request):
    return render(request,"HII/index.html")

def kevin(request):
    return HttpResponse("Hello Kevin")

def greet(request, name ):
    data = {
        'name': name
    }
    return render(request,"HII/greet.html",data)

