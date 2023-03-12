from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from BearHubHome.models import Student, Event, AdminUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
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
    if request.method == "POST":
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
                    return HttpResponseRedirect(reverse("bear:stupage", args=[user.pk]))
                else:
                    print("wrong credintals")
                    form.add_error('id', 'You seem to have entered in incorrect credintials. Please try again')
                    error_message = form.errors['id'][0]
                    return render(request, "HII/StudentPage.html", {"form": form, "error_message": error_message})    
            except (Student.DoesNotExist, ValueError):
                form.add_error('id', 'You seem to have entered in incorrect credintials. Please try again')
                error_message = form.errors['id'][0]
                return render(request, "HII/StudentPage.html", {"form": form, "error_message": error_message})
        else:
            form = LogInForm()
    return render(request, "HII/StudentPage.html", {"form": LogInForm()})
def StudentPage(request, user_id):
    try:
        user = Student.objects.get(pk=user_id)
        
        events = user.event.all()
        Nonevents = Event.objects.exclude(id__in=user.event.all().values_list('id', flat=True))

        return render(request, "HII/signedIn.html", {"user": user,"events": events,"Nonevents":Nonevents})

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
            if Student.objects.filter(pk=idIn).exists():
                error_message = "This student ID is already taken. Please enter a different ID."
                return render(request, "HII/signUp.html", {"form": form, "error_message": error_message})
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
def adminLogIn(request):
        if request.method == "POST":
            form = LogInForm(request.POST)
            if form.is_valid():
                passwordIn = form.cleaned_data.get("password")
                idIn = form.cleaned_data.get("id")
                # next step check if the data is correct and sign the user into the signed in page
                try:
                    user = AdminUser.objects.get(pk=idIn)
                    if user.password == passwordIn:
                        # The password is correct, so the user is authenticated
                        return HttpResponseRedirect(reverse("bear:adpage", args=[user.pk]))
                    else:
                        form.add_error('id', 'You seem to have entered in incorrect credintials. Please try again')
                        error_message = form.errors['id'][0]
                        return render(request, "HII/AdminLogIn.html", {"form": form, "error_message": error_message})    
                except (AdminUser.DoesNotExist, ValueError):
                    form.add_error('id', 'You seem to have entered in incorrect credintials. Please try again')
                    error_message = form.errors['id'][0]
                    return render(request, "HII/AdminLogIn.html", {"form": form, "error_message": error_message})
            else:
                form = LogInForm()
        return render(request, "HII/AdminLogIn.html", {"form": LogInForm()})
def AdminPage(request, user_id):
    try:
        user = AdminUser.objects.get(pk=user_id)
        events = Event.objects.all()
        return render(request, "HII/AdminPage.html", {"user": user, "events": events})
    except AdminUser.DoesNotExist:
        return HttpResponseRedirect(reverse("bear:adminLogIn"))
def Update(request):

    if request.method == 'POST':
        values = json.loads(request.body)
        
        for value in values:
            # update the event with the specified values
            # (assuming you have an Event model with name, date, description, and point_value fields)
            event = Event.objects.get(name=value['name'])
            event.description = value['description']
            event.point_value = value['point_value']
            event.name=value['name']

            event.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
def NewEvent(request):

    if request.method == 'POST':
        values = json.loads(request.body)
        
        for value in values:
            # update the event with the specified values
            # (assuming you have an Event model with name, date, description, and point_value fields)
            
            description = value['description']
            point_value = value['point_value']
            name=value['name']
            date=value['date']
            event = Event.objects.create(
                description=description,
                point_value=point_value,
                name=name,
                date=date,
            )    
            event.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
def requestEvent(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        student_id = request.POST.get('user_id')
        print(event_id)
        print(student_id)
        event= Event.objects.get(id=event_id)
        student= Student.objects.get(id=student_id)
        # Add the event to the student's events
        student.event.add(event)
        
        # add event to user's requests (you'll need to define this logic yourself)
        return StudentPage(request,student_id)

    # if the request is not a POST request, render the events list template
    
    return JsonResponse({'success': False, 'error': 'Get request'})