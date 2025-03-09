from django.contrib import admin
from django.urls import path, include
from events_app.views import events_view
from social_app.views import buddyup_view
from users_app.views import login_view, home_view, profile_view, verification_prompt_view, logout_view, edit_profile_view
from django.conf import settings
from django.conf.urls.static import static

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
#<!-- # <a href="{% url 'contact' %}">CONTACT US</a>     we will need a contact us page -->

    # REDIRECT PAGES
    path('verification/', verification_prompt_view, name='verification'),
    path('logout/', logout_view, name='logout'),


     path('profile/edit/', edit_profile_view, name='edit_profile'),
]


# Development only: serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)