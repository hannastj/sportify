from django.shortcuts import render, redirect 
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from social_app.models import BuddyRequest
from .forms import RegistrationForm 
from events_app.models import WorkoutEvent
from .forms import ProfileUpdateForm
from django.utils import timezone
from django.db.models import Q
from events_app.forms import WorkoutEventForm
from django.contrib import messages



#----------------------- LOGIN/SIGNUP PAGE --------------------------
def login_view(request):
    login_form = AuthenticationForm()
    register_form = RegistrationForm()

    if request.method == "POST":
        if "register" in request.POST:  # Registration form
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                register_form.save()  # Save user
                messages.success(request, "Registration successful, please log in!")
                return redirect("login")

            
        elif "login" in request.POST:  # Login form
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("home")

            else:
                return render(request, "users_app/login.html", {
                    "error_message": "Invalid credentials. Please try again or sign up.",
                    "login_form": login_form,
                    "register_form": register_form
                })
    
    return render(request, "users_app/login.html", {
        "login_form": login_form, 
        "register_form": register_form
    })

#----------------------- HOME PAGE  ----------------------------
@login_required
def home_view(request):
    next_event = None
    if request.user.is_authenticated:
        now = timezone.now()
        # Retrieve events where the user is the host or a participant,
        # and the event's start time is in the future.
        upcoming_events = WorkoutEvent.objects.filter(
            Q(host=request.user) | Q(participants=request.user),
            start_time__gte=now
        ).order_by('start_time')
        if upcoming_events.exists():
            next_event = upcoming_events.first()
    return render(request, 'users_app/home.html', {'next_event': next_event})

#----------------------- PROFILE PAGE  ----------------------------

@login_required
def profile_view(request):
    if request.method == "POST" and 'create_event' in request.POST:
        event_form = WorkoutEventForm(request.POST)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.host = request.user  # Set the current user as the host
            new_event.save()
            return redirect('profile')
    else:
        event_form = WorkoutEventForm()

    # Filter events so that only upcoming ones are included
    hosted_events = WorkoutEvent.objects.filter(
        host=request.user, 
        start_time__gte=timezone.now()
    )
    participated_events = request.user.participated_events.filter(
        start_time__gte=timezone.now()
    ).exclude(host=request.user)
    context = {
        'user': request.user,
        'hosted_events': hosted_events,
        'participated_events': participated_events,
        'event_form': event_form,
        'buddy_incoming_requests': BuddyRequest.objects.filter(status="pending", receiver=request.user.id),
        }

    
    return render(request, 'users_app/profile.html', context)

#----------------------- EDIT PROFILE --------------------------

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  
            return redirect('profile')  
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users_app/edit_profile.html', {'form': form})

#----------------------- LOGOUT --------------------------

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")  



