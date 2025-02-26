from django.urls import path

from events_app.views import search_events_view
from . import views
import events_app

app_name = 'sportify_app'

urlpatterns = [
    path('buddy-requests/', views.buddy_requests_list_view, name='buddy_requests'),
    path('buddy-requests/send/<int:user_id>/', views.send_buddy_request_view, name='send_buddy_request'),
    path('buddy-requests/respond/<int:request_id>/', views.respond_buddy_request_view, name='respond_buddy_request'),
    path('search/users/', views.search_users_view, name='search_users'),
    path('search/events/', search_events_view, name='search_events'),
]