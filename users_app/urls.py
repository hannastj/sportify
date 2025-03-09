from django.urls import path
from .views import login_view, home_view, logout_view, edit_profile_view

app_name = 'users_app'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),

    path('edit/', edit_profile_view, name='edit_profile'),
    
]
