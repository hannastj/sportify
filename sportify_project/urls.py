from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from events_app.views import events_view
from social_app.views import buddyup_view, buddy_list_view, buddy_profile_view
from django.conf import settings
from django.conf.urls.static import static
from users_app.views import login_view, home_view, profile_view, verification_prompt_view, logout_view, edit_profile_view

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

    # REDIRECT PAGES
    path('logout/', logout_view, name='logout'),
    path('buddylist/', buddy_list_view, name='buddyup'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('buddy/<int:user_id>/', buddy_profile_view, name='buddy_profile'),
    path('ajax/buddy-search/', buddyup_view, name='buddy_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)