from django.contrib import admin
from django.urls import path, include
from events_app.views import events_view
from social_app.views import buddyup_view
from users_app.views import login_view, home_view


urlpatterns = [
    path('admin/', admin.site.urls),



    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('events/', events_view, name='events'),
    path('buddyup/', buddyup_view, name='buddyup'),



    path('events/', include('events_app.urls')),
    path('social/', include('social_app.urls')),
    path('users/', include('users_app.urls')),
]
