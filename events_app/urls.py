from django.urls import path
from events_app import views

app_name = 'events_app'

urlpatterns = [
    path('search-events/', views.search_events_view, name='search_events'),
    path('events/', views.event_feed_view, name='event_feed'),
    path('events/create/', views.create_event_view, name='create_event'),
    path('events/<int:event_id>/join/', views.join_event_view, name='join_event'),
    path('events/<int:event_id>/leave/', views.leave_event_view, name='leave_event'),
]