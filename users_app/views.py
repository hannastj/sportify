from django.shortcuts import render

def index(request):
    context = {'boldmessage': 'Hello from Sportify!'}
    return render(request, 'index.html', context)

#----------------------- ABOUT PAGE  ----------------------------
def about_view(request):
    return render(request, 'about.html')

#----------------------- LOGIN/SIGNUP PAGE --------------------------
def login_signup_view(request):
    context = {}
    return render(request, 'login.html')


