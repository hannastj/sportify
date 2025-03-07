from django.urls import path
from .views import login_view, home_view, logout_view
from django_email_verification import verify

app_name = 'users_app'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'), #IZZAK: For consistency rename about to Home
    path('logout/', logout_view, name='logout'),
    path("verify/<str:token>/", verify, name="email_verification"), #IZZAK: for email veriication
]