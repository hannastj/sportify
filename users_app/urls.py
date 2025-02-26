from django.urls import path
from . import views

app_name = 'sportify_app'

urlpatterns = [
    path('login/', views.login_signup_view, name='login'),
]