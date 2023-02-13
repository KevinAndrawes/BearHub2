from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django import forms
from BearHubHome.models import Student
# Create your views here.
class LogInForm(forms.Form):
    id = forms.CharField(label="id")
    password = forms.CharField(label="password")
def index(request):
    if request.method=="POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            passwordIn = form.cleaned_data.get("password")
            idIn = form.cleaned_data.get("id")
            # next step check if the data is correct and sign the user into the signed in page
            try:
                user = Student.objects.get(pk=idIn)
                if user.password == passwordIn:
                    # The password is correct, so the user is authenticated
                    # ...
                    print("Ur in")
                else:
                    print("wrong credintals")    
            except Student.DoesNotExist:
                print("Studen doesnt exist")
                
                
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


  