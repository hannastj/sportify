from django.urls import path
from social_app import views
from .views import buddy_details_ajax

app_name = 'social_app'

urlpatterns = [
    path('buddyup/', views.buddyup_view, name='buddyup'),
    path('buddy-requests/', views.buddy_requests_list_view, name='buddy_requests'),
    path('buddy-requests/send/<int:user_id>/', views.send_buddy_request_view, name='send_buddy_request'),
    path('buddy-requests/respond/<int:request_id>/', views.respond_buddy_request_view, name='respond_buddy_request'),
    path('search-users/', views.search_users_view, name='search_users'),
    path('buddy-list/', views.buddy_list_view, name='buddy_list'),
    path('ajax/buddy-details/<int:buddy_id>/', buddy_details_ajax, name='buddy_details_ajax'),
]