from django.contrib import admin
from django.urls import path, include
from events_app.views import events_view
from social_app.views import buddyup_view
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from users_app.views import login_view, home_view, profile_view, verification_prompt_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),

    path('events/', include('events_app.urls')),
    path('social/', include('social_app.urls')),
    path('users/', include('users_app.urls')),

    # MAIN PAGES
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('buddyup/', buddyup_view, name='buddyup'),
    path('profile/', profile_view, name='profile'),
    path('events/', events_view, name= 'events'),

    # REDIRECT PAGES
    path('verification/', verification_prompt_view, name='verification'),
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    ]