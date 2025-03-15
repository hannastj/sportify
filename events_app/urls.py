from django.urls import path
from . import views

app_name = 'events_app'

urlpatterns = [
    path('', views.events_view, name='events'),
    path('create/', views.create_event_view, name='create_event'), 
    path('search-events/', views.search_events_view, name='search_events'),
    path('<int:event_id>/join/', views.join_event_view, name='join_event'), 
    path('<int:event_id>/leave/', views.leave_event_view, name='leave_event'), 
    path('my/', views.my_events_view, name='my_events'),
]
