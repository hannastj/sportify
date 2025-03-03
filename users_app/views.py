from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

#----------------------- HOME PAGE  ----------------------------
def home_view(request):
    return render(request, 'home.html')

#----------------------- LOGIN/SIGNUP PAGE --------------------------
def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['error'] = "Invalid username or password."

    return render(request, 'login.html', context)
