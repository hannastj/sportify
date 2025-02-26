from django.urls import path
from . import views

app_name = 'sportify_app'

urlpatterns = [
    path('events/', views.event_feed_view, name='event_feed'),
    path('events/create/', views.create_event_view, name='create_event'),
    path('events/<int:event_id>/join/', views.join_event_view, name='join_event'),
    path('events/<int:event_id>/leave/', views.leave_event_view, name='leave_event'),
]