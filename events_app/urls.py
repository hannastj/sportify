from django.urls import path
from events_app import views

app_name = 'events_app'

urlpatterns = [
    path('search-events/', views.search_events_view, name='search_events'),
    path('events/', views.events_view, name='events'),
    path('events/create/', views.create_event_view, name='create_event'),
    path('events/<int:event_id>/join/', views.join_event_view, name='join_event'),
    path('events/<int:event_id>/leave/', views.leave_event_view, name='leave_event'),
]