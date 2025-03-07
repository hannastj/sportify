from django.shortcuts import render, redirect 
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required 
from .forms import RegistrationForm 
from .models import CustomUser 

#----------------------- HOME PAGE  ----------------------------
def home_view(request):
    return render(request, 'users_app/home.html')

#----------------------- PROFILE PAGE  ----------------------------
@login_required
def profile_view(request):
    return render(request, 'users_app/profile.html')

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
                    "error": "Invalid credentials. Please try again or sign up.",
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
