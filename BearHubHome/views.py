import random
import string
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from BearHubHome.models import RewardRequest, Student, Event, AdminUser, EventRequest, Reward
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg

class LogInForm(forms.Form):# form for longing in
    id = forms.CharField(label="ID")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

#Class to sign up and create new user.
class SignUpForm(forms.Form):
    firstName = forms.CharField(label="First Name")
    lastName = forms.CharField(label="Last Name")
    id = forms.CharField(label="School ID")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Re-Enter Your Password", widget=forms.PasswordInput())
    email = forms.CharField(label="Email Address")
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
    # Try to retrieve a student instance with the given user_id
    try:
        user = Student.objects.get(pk=user_id)
        # Retrieve all events for this student and order them by date
        events = user.event.all().order_by('date')
        # Retrieve all events that the student hasn't signed up for yet and order them by date
        Nonevents = Event.objects.exclude(id__in=user.event.all().values_list('id', flat=True)).order_by('date')
        # Retrieve all rewards
        Rewards = Reward.objects.all()
        # Render the signedIn.html template with the retrieved data
        return render(request, "HII/signedIn.html", {"user": user, "events": events, "Nonevents": Nonevents, "Rewards": Rewards})
    # If the student doesn't exist, redirect to the login page
    except Student.DoesNotExist:
        return HttpResponseRedirect(reverse("bear:LogIn"))
def events(request, user_id):
    # Try to retrieve a student instance with the given user_id
    try:
        user = Student.objects.get(pk=user_id)
        # Retrieve all events for this student and order them by date
        events = user.event.all().order_by('date')
        # Retrieve all events that the student hasn't signed up for yet and order them by date
        Nonevents = Event.objects.exclude(id__in=user.event.all().values_list('id', flat=True)).order_by('date')
        # Render the signedIn.html template with the retrieved data
        return render(request, "HII/events.html", {"user": user, "events": events, "Nonevents": Nonevents})
    # If the student doesn't exist, redirect to the login page
    except Student.DoesNotExist:
        return HttpResponseRedirect(reverse("bear:LogIn"))
def SignUp(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():# getting all data
            passwordIn = form.cleaned_data.get("password")
            password2In = form.cleaned_data.get("password2")
            idIn = form.cleaned_data.get("id")
            firstname = form.cleaned_data.get("firstName")
            lastname = form.cleaned_data.get("lastName")
            Grade_level = form.cleaned_data.get("Grade_level")
            email = form.cleaned_data.get("email")
            if passwordIn and password2In and passwordIn != password2In:#checking if both passwords match
                error_message = "These passwords do not match."
                return render(request, "HII/signUp.html", {"form": form, "error_message": error_message})
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
                points= 0,
                Email= email
            )
            # Redirect to the StudentPage with the new student's ID
            return HttpResponseRedirect(reverse("bear:stupage", args=[user.id]))
    else:
        form = SignUpForm()
    return render(request, "HII/signUp.html", {"form": form})

def index(request):
    users = Student.objects.order_by('-points')
    allevents = Event.objects.order_by('date')
    return render(request,"HII/index.html", {"users": users})
def get_events(request):# gets the events to be displayed on the calender
    events = Event.objects.all()#grabbing all the events from the database
    data = []
    for event in events:#looping through all events
        data.append({# data being sent
            'title': event.name,
            'start': event.date.isoformat(),
            'description': event.description,
        })
    return JsonResponse(data, safe=False)#returning the data to the javascript function
def help(request):
    return render(request,"HII/help.html")
def adminLogIn(request):#The method for admins
        if request.method == "POST":# when the log-in button is pressed
            form = LogInForm(request.POST)
            if form.is_valid():#getting data
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
def AdminPage(request, user_id):# Requesting admin page 
    try:
        user = AdminUser.objects.get(pk=user_id)
        events = Event.objects.all().order_by('date')
        eventRequests = EventRequest.objects.all()
        return render(request, "HII/AdminPage.html", {"user": user, "events": events,"eventRequests":eventRequests})
    except AdminUser.DoesNotExist:# Handling if the user id doesn't match to an admin
        return HttpResponseRedirect(reverse("bear:adminLogIn"))
def Update(request):# update events
    if request.method == 'POST':
        values = json.loads(request.body)
        for value in values:# Updating all the events that got changed
            # update the event with the specified values
            event = Event.objects.get(name=value['name'])
            event.date = value['date']
            event.description = value['description']
            event.point_value = value['point_value']
            event.name=value['name']

            event.save()# Saving in the database
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
def NewEvent(request):
    # 
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
from django.http import JsonResponse

def requestEvent(request):
    # Allows Student to request for points if student attended the event
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        student_id = request.POST.get('user_id')
        Event1 = Event.objects.get(id=event_id)
        Student1 = Student.objects.get(id=student_id)
        # Add the event to the student's events
        Student1.event.add(Event1)
        existing_request = EventRequest.objects.filter(student=Student1, Event=Event1).exists()
        if existing_request:
            return StudentPage(request,student_id)
        newRequest = EventRequest.objects.create(
            student=Student1,
            Event=Event1
        )
        newRequest.save()
        return StudentPage(request,student_id)
    # if the request is not a POST request, return an error response
    return StudentPage(request,student_id)


def accept_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request_id = data.get('requestId')
        action = data.get('action')
        event_request = EventRequest.objects.get(id=request_id)
        student = event_request.student
        event = event_request.Event
        if action == 'accept':
            student.points += event.point_value
            student.save()
            event_request.delete()
            # send accept email to student
            subject = 'Event Request Accepted'
            from_email = 'BearHubConfirmation@gmail.com'
            recipient_list = [student.Email]
            # Render the HTML email template
            html_message = render_to_string('HII/eventEmail.html', {'student': student, 'event': event})
                # Send the email
            send_mail(subject, None, from_email, recipient_list, html_message=html_message)
            return JsonResponse({'success': True})
        elif action == 'decline':
            event_request.delete()
            # send decline email to student
            subject = 'Event Request Declined'
            html_message = render_to_string('HII/eventEmailDec.html', {'student': student, 'event': event})
            from_email = 'BearHubConfirmation@gmail.com'
            recipient_list = [student.Email]
            send_mail(subject, None, from_email, recipient_list, html_message=html_message)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def claim_reward(request):
    reward_id = request.POST.get('reward_id')
    student_id = request.POST.get('student_id')
    reward = get_object_or_404(Reward, id=reward_id)
    student = get_object_or_404(Student,id=student_id)  # Assuming the logged in user is a student
    if student.points >= reward.point_value:
        #If student points are greater than the cost of the reward than award the student & email
        student.points -= reward.point_value
        student.save()
        subject = 'Reward'
        newRewardRequest = RewardRequest.objects.create(Key=''.join(random.choices(string.digits, k=10)))
        html_message = render_to_string('HII/reward.html', {'student': student, 'Reward': reward, 'rewardRequest': newRewardRequest})
        from_email = 'BearHubConfirmation@gmail.com'
        recipient_list = [student.Email]
        send_mail(subject, None, from_email, recipient_list, html_message=html_message)
        # Add code to handle giving the reward to the student
    else:
        # Handle case where student doesn't have enough points
        pass
    return StudentPage(request,student_id)
def checkReward(request): # Checking if the code is valid that the admin enters
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('searchValue')
        try:
            rewardRequest = RewardRequest.objects.get(Key=key)
            rewardRequest.delete()
            return JsonResponse({'message': 'This code is correct, this code is no longer valid!'})
        except RewardRequest.DoesNotExist:
            return JsonResponse({'message': 'Sorry, that code is incorrect.'})
def report(request):
    users = Student.objects.order_by('-points')
    users9 = Student.objects.filter(grade_level=9).order_by('-points')
    users10 = Student.objects.filter(grade_level=10).order_by('-points')
    users11 = Student.objects.filter(grade_level=11).order_by('-points')
    users12 = Student.objects.filter(grade_level=12).order_by('-points')

    avg9 = users9.aggregate(Avg('points'))['points__avg']
    avg10 = users10.aggregate(Avg('points'))['points__avg']
    avg11 = users11.aggregate(Avg('points'))['points__avg']
    avg12 = users12.aggregate(Avg('points'))['points__avg']
    avg = users.aggregate(Avg('points'))['points__avg']

    total9 = users9.aggregate(Sum('points'))['points__sum']
    total10 = users10.aggregate(Sum('points'))['points__sum']
    total11 = users11.aggregate(Sum('points'))['points__sum']
    total12 = users12.aggregate(Sum('points'))['points__sum']
    total = users.aggregate(Sum('points'))['points__sum']
    random_winner = []
    for students in [users9, users10, users11, users12]:
        if students.exists():
            random_winner.append(random.choice(students))

    # selecting the student with the highest points in each grade level
    highest_point_students = []
    for grade_level in [9, 10, 11, 12]:
        student = Student.objects.filter(grade_level=grade_level).order_by('-points').first()
        highest_point_students.append(student)
    context = {
        "users": users,
        "users9": users9,
        "users10": users10,
        "users11": users11,
        "users12": users12,
        "avg9": round(avg9) if avg9 else 0,
        "avg10": round(avg10) if avg10 else 0,
        "avg11": round(avg11) if avg11 else 0,
        "avg12": round(avg12) if avg12 else 0,
        "avg": round(avg) if avg else 0,
        "total9": total9 if total9 else 0,
        "total10": total10 if total10 else 0,
        "total11": total11 if total11 else 0,
        "total12": total12 if total12 else 0,
        "total": total if total else 0,
        "random_winner":random_winner,
        "higest_point_students":highest_point_students
    }

    return render(request, "HII/report.html", context)