from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
    CHOICES = [
        ('9', '9th grade'),
        ('10', '10th grade'),
        ('11', '11th grade'),
        ('12', '12th grade'),
    ]
    Grade_level = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,label="Grade Level:")
def LogIn(request):
    SignedIn = False
    if request.method=="POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            passwordIn = form.cleaned_data.get("password")
            idIn = form.cleaned_data.get("id")
            # next step check if the data is correct and sign the user into the signed in page
            try:

                user = Student.objects.get(pk=idIn)
                if user.password == passwordIn:
                    SignedIn = True
                    # The password is correct, so the user is authenticated
                    # Make it so when the user enters in a invalid type it doesn't crash
                    return HttpResponseRedirect(reverse("bear:stupage", args=[user.pk]))
                else:
                    print("wrong credintals")    
            except Student.DoesNotExist:
                print("Studen doesnt exist")
   
                
        else:
            form = LogInForm()
    return render(request,"HII/StudentPage.html",{"form":LogInForm()})
def StudentPage(request, user_id):
    try:
        user = Student.objects.get(pk=user_id)
        return render(request, "HII/signedIn.html", {"user": user})

    except Student.DoesNotExist:
        return HttpResponseRedirect(reverse("bear:LogIn"))

def SignUp(request):

    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            passwordIn = form.cleaned_data.get("password")
            idIn = form.cleaned_data.get("id")
            firstname = form.cleaned_data.get("firstName")
            lastname = form.cleaned_data.get("lastName")
            Grade_level = form.cleaned_data.get("Grade_level")
            # Create a new Student object with the submitted data
            user = Student.objects.create(
                id=idIn,
                password=passwordIn,
                First_name=firstname,
                Last_name=lastname,
                grade_level= Grade_level,
                points= 0
            )
            # Redirect to the StudentPage with the new student's ID
            return HttpResponseRedirect(reverse("bear:stupage", args=[user.id]))
    else:
        form = SignUpForm()
    return render(request, "HII/signUp.html", {"form": form})

def kevin(request):
    return HttpResponse("Hello Kevin")
def index(request):
    return render(request,"HII/index.html")


