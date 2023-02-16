from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django import forms
from django.urls import reverse
from BearHubHome.models import Student
from django.contrib.auth.decorators import login_required
# Create your views here.
class LogInForm(forms.Form):
    id = forms.CharField(label="ID")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

#Class to sign up and create new user.
class SignUpForm(forms.Form):
    firstName = forms.CharField(label="First Name")
    lastName = forms.CharField(label="Last Name")
    id = forms.CharField(label="School ID")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    username = forms.CharField(label="Username")
    CHOICES = [
        ('choice9', '9th grade'),
        ('choice10', '10th grade'),
        ('choice11', '11th grade'),
        ('choice12', '12th grade'),
    ]
    grade_level = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


def StudentPage(request, user_id):
    try:
        user = Student.objects.get(pk=user_id)
        print(user.points)
        return render(request, "HII/signedIn.html", {"user": user})

    except Student.DoesNotExist:
        return HttpResponseRedirect(reverse("bear:index"))

def index(request):
    SignedIn = False
    if request.method=="POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            passwordIn = form.cleaned_data.get("password")
            idIn = form.cleaned_data.get("id")
            # next step check if the data is correct and sign the user into the signed in page
            try:

                user = Student.objects.get(pk=idIn)
                print(user.pk)
                if user.password == passwordIn:
                    SignedIn = True
                    # The password is correct, so the user is authenticated
                    # Make it so when the user enters in a invalid type it doesn't crash
                    print("Ur in")
                    return HttpResponseRedirect(reverse("bear:stupage", args=[user.pk]))
                else:
                    print("wrong credintals")    
            except Student.DoesNotExist:
                print("Studen doesnt exist")
                
                
        else:
            form = LogInForm()
    return render(request,"HII/index.html",{"form":LogInForm()})

def kevin(request):
    return HttpResponse("Hello Kevin")

def SignUp(request):
    return render(request,"HII/signUp.html")

