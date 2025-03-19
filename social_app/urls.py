from django.urls import path
from social_app import views
from .views import buddy_details_ajax, buddyup_view, buddy_profile_view, buddy_search_view, send_buddy_request_view, \
    send_buddy_request_ajax, respond_buddy_request_view

app_name = 'social_app'

urlpatterns = [
    path('buddyup/', views.buddy_list_view, name='buddyup'),


    path('ajax/buddy-details/<int:buddy_id>/', buddy_details_ajax, name='buddy_details_ajax'),
    path('ajax/buddy-search/',buddy_search_view, name='buddy_search'),
    path('ajax/send-buddy-request/', send_buddy_request_ajax, name='send_buddy_request_ajax'),


    path('buddy/<int:user_id>/', buddy_profile_view, name='buddy_profile'),
    path('buddy-requests/', views.buddy_requests_list_view, name='buddy_requests'),
    path('buddy-requests/send/', send_buddy_request_view, name='send_buddy_request'),
    path('buddy-requests/respond_buddy_request/<int:request_id>/', respond_buddy_request_view, name='respond_buddy_request'),
]