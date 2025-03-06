from django.shortcuts import render, redirect #IZZAK: redirect users to another page
from django.contrib.auth import login, logout, authenticate #IZZAK: These are built-in Django functions for authentication functions
from django.contrib.auth.forms import AuthenticationForm #IZZAK: built in login form 
from django.contrib.auth.decorators import login_required #IZZAK: This retricts certains views to logged-in users only
from .forms import RegistrationForm #IZZAK: This is the form from forms.py
from .models import CustomUser #IZZAK: This is the user from model.py
from django_email_verification import send_email #IZZAK: This sends the email with the link to new users to verify them


#----------------------- HOME PAGE  ----------------------------
def home_view(request):
    return render(request, 'home.html')

#----------------------- PROFILE PAGE  ----------------------------
def profile_view(request):
    return render(request, 'profile.html')

#----------------------- VERIFICATION PROMPT  ----------------------------
def verification_prompt_view(request):
    return render(request, "verification_prompt.html")

#----------------------- LOGIN/SIGNUP PAGE --------------------------
def login_view(request):
    #IZZAK: The two forms that will be on this page
    login_form = AuthenticationForm() # This is the built-in login form django provides
    register_form = RegistrationForm() # This is the form i have created for registration

    #IZZAK: if the user submites the form
    if request.method == "POST":

        #IZZAK: since there are two forms we must differenciate between them
        if "register" in request.POST: #Registration form
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False) #creates user object but doesn't save it yet as we need to disable is_active so they can't login
                user.is_active = False #This disables login until email verification
                user.save()
                send_email(user)
                return render(request, "verify_prompt.html") # This is a new page that informs new users to check their email. Does not need to be added to path as it is not a page. just a html screen
            
        #IZZAK: Now check login stuff
        elif "login" in request.POST:
            login_form = AuthenticationForm(data=request.POST) # Validate login
            if login_form.is_valid():
                user = login_form.get_user()
                if user.is_email_verified:
                    login(request, user)
                    return redirect("about") #IZZAK: For consistency rename about to Home
                else:
                    return render(request, "login.html", {
                        "error": "Please verify your email before logging in.",
                        "login_form": login_form,
                        "register_form": register_form
                    })
                
    return render(request, "login.html", {"login_form": login_form, "register_form": register_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login") # Redirects to login