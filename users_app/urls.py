from django.urls import path
from .views import login_view, home_view, logout_view, profile_view

app_name = 'users_app'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]
