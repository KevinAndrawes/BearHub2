from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django import forms
# Create your views here.
class LogInForm(forms.Form):
    id = forms.CharField(label="id")
    password = forms.CharField(label="password")
def index(request):
    if request.method=="POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            id = form.cleaned_data.get("id")

        else:
            form = LogInForm()
    return render(request,"HII/index.html",{"form":LogInForm()})

def kevin(request):
    return HttpResponse("Hello Kevin")

def greet(request, name ):
    data = {
        'name': name
    }
    return render(request,"HII/greet.html",data)


  