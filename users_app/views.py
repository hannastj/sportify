from django.shortcuts import render, redirect 
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required 
from .forms import RegistrationForm 
from .models import CustomUser 
from django import forms
from events_app.models import WorkoutEvent
from .forms import ProfileUpdateForm

#----------------------- HOME PAGE  ----------------------------
def home_view(request):
    return render(request, 'users_app/home.html')

#----------------------- PROFILE PAGE  ----------------------------
@login_required
def profile_view(request):
    hosted_events = WorkoutEvent.objects.filter(host=request.user)
    participated_events = request.user.participated_events.all()
    context = {
        'user': request.user,
        'hosted_events': hosted_events,
        'participated_events': participated_events,
    }
    return render(request, 'users_app/profile.html', context)

#Stuff for profile page will be here!!


#---------------------- EDIT PROFILE ------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'age', 'bio', 'clubs')  # add any extra fields here

#----------------------- VERIFICATION PROMPT  ----------------------------
def verification_prompt_view(request):
    return render(request, 'users_app/verification_prompt.html')

#----------------------- LOGIN/SIGNUP PAGE --------------------------
def login_view(request):
    login_form = AuthenticationForm()
    register_form = RegistrationForm()

    if request.method == "POST":
        if "register" in request.POST:  # Registration form
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                register_form.save()  # Save user
                return redirect("login")  # Redirect instead of rendering
            
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

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")  


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  # This updates the user's fields, M2Ms, and saves the image
            return redirect('profile')  # Or wherever you want them to go
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users_app/edit_profile.html', {'form': form})