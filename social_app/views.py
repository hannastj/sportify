from django.shortcuts import redirect,get_object_or_404,render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from social_app import models
from users_app.models import CustomUser
from django.http import JsonResponse, Http404

#----------------------- BUDDYUP PAGE  ----------------------------
def buddyup_view(request):
    return render(request, 'social_app/buddyup.html')

#---------------- SENDING A BUDDY REQUEST ---------------------
def send_buddy_request_view(request, user_id):
    if request.method == 'POST':
        receiver = get_object_or_404(User, pk=user_id)
        models.BuddyRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver,
            defaults={'status': 'pending'}
        )
    return redirect('profile', user_id=user_id)

#---------------- ACCEPT OR DECLINE BUDDY REQUEST ---------------------
def respond_buddy_request_view(request, request_id):
    if request.method == 'POST':
        buddy_req = get_object_or_404(models.BuddyRequest, id=request_id, receiver=request.user)
        action = request.POST.get('action')  #USER ENTERS 'ACCEPT' OR 'DECLINE'
        if action == 'accept':
            buddy_req.status = 'accepted'
        elif action == 'reject':
            buddy_req.status = 'rejected'
        buddy_req.save()
    return redirect('buddy_requests_list')

#---------------- PENDING BUDDY REQUESTS ---------------------
def buddy_requests_list_view(request):
    incoming = models.BuddyRequest.objects.filter(receiver=request.user, status='pending')
    outgoing = models.BuddyRequest.objects.filter(sender=request.user, status='pending')
    return render(request, 'social_app/buddy_requests.html', {'incoming': incoming, 'outgoing': outgoing})

#---------------- BUDDY SEARCH ---------------------
def search_buddy_view(request):
    # We'll assume you pass the query as a GET param named 'q'
    query = request.GET.get('q', '')
    UserModel = get_user_model()

    # Filter users by username (case-insensitive)
    # e.g., if query = 'kerr', matches 'Kerr', 'kerrigan', etc.
    buddies = UserModel.objects.filter(username__icontains=query)

    # Build a list of dicts to return as JSON
    results = []
    for buddy in buddies:
        results.append({
            'id': buddy.id,
            'username': buddy.username,
            'age': buddy.age if hasattr(buddy, 'age') else None,
            # or any other fields you want
        })

    return JsonResponse({'results': results})


#---------------- BUDDY PROFILE VIEW ---------------------
def buddy_profile_view(request, user_id):
    UserModel = get_user_model()
    buddy = get_object_or_404(UserModel, pk=user_id)
    return render(request, 'social_app/buddy_profile.html', {'buddy': buddy})

#---------------- BUDDY LISTING  ---------------------
def buddy_list_view(request):
    buddies = CustomUser.objects.all()
    return render(request, 'social_app/buddyup.html', {'buddies': buddies})

#---------------- BUDDY LISTING DETAIL (AJAX) ---------------------

def buddy_details_ajax(request, buddy_id):
    try:
        buddy = CustomUser.objects.get(pk=buddy_id)
    except CustomUser.DoesNotExist:
        raise Http404("Buddy not found")
    data = {
        'username': buddy.username,
        'age': buddy.age,
        'bio': buddy.bio
    }
    return JsonResponse(data)