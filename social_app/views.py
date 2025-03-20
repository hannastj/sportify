from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,get_object_or_404,render
from django.contrib.auth.models import User

from events_app.models import WorkoutEvent
from social_app import models
from social_app.models import BuddyRequest
from users_app.models import CustomUser
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST


#----------------------- BUDDYUP PAGE ----------------------------
def buddyup_view(request):
    return render(request, 'social_app/buddyup.html')

#---------------- SENDING A BUDDY REQUEST ---------------------
@login_required
@require_POST
def send_buddy_request_view(request):
    buddy_id = request.POST.get('buddy_id')
    if not buddy_id:
        return HttpResponseBadRequest("No buddy_id provided")

    UserModel = get_user_model()
    receiver = get_object_or_404(UserModel, pk=buddy_id)
    # Create or get an existing request
    BuddyRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status': 'pending'}
    )
    # Redirect or return JSON
    return JsonResponse({'message': 'Buddy request sent', 'buddy_id': buddy_id})

#---------------- ACCEPT OR DECLINE A REQUEST ---------------------
@login_required
@require_POST
def respond_buddy_request_view(request: object, request_id: int) -> JsonResponse:

    print(request_id)
    buddy_req = get_object_or_404(BuddyRequest, id=request_id)
    action = request.POST.get('action')  # "accept" or "reject"

    if action == 'accept':
        buddy_req.status = 'accepted'
        buddy_req.sender.buddies.add(buddy_req.receiver)
        buddy_req.receiver.buddies.add(buddy_req.sender)
        buddy_req.save()

    elif action == 'reject':
        buddy_req.status = 'rejected'
        buddy_req.save()

    return buddy_profile_view(request, request.user.id, f"Buddy ({buddy_req.sender}) request {action}ed")

#---------------- PENDING BUDDY REQUESTS ---------------------
def buddy_requests_list_view(request):
    incoming = models.BuddyRequest.objects.filter(receiver=request.user, status='pending')
    outgoing = models.BuddyRequest.objects.filter(sender=request.user, status='pending')
    return render(request, 'social_app/buddy_requests.html', {'incoming': incoming, 'outgoing': outgoing})

#---------------- BUDDY SEARCH ---------------------
@require_GET
def buddy_search_view(request):
    query = request.GET.get('q', '').strip()
    UserModel = get_user_model()

    if query:
        buddies = UserModel.objects.filter(
            Q(username__icontains=query)
        ).distinct()

    else:
        buddies = UserModel.objects.none()
    user_list = []
    for buddy in buddies:
        user_list.append({
            'id': buddy.id,
            'username': buddy.username,
            'age': buddy.age if hasattr(buddy, 'age') else None,
            'bio': buddy.bio if hasattr(buddy, 'bio') else '',
        })

    return JsonResponse({'users': user_list})

#---------------- BUDDY PROFILE VIEW ---------------------
def buddy_profile_view(request, user_id, message=None):
    buddy = get_object_or_404(CustomUser, pk=user_id)
    hosted_events = WorkoutEvent.objects.filter(host=buddy)
    participated_events = WorkoutEvent.objects.filter(participants=buddy)

    # Only show incoming buddy requests if the logged-in user is the profile owner.
    if request.user == buddy:
        buddy_incoming_requests = BuddyRequest.objects.filter(receiver=request.user, status='pending')
    else:
        buddy_incoming_requests = None

    return render(request, 'users_app/profile.html', {
        'user': buddy,
        'hosted_events': hosted_events,
        'participated_events': participated_events,
        'message':message,
        'buddy_incoming_requests': buddy_incoming_requests,
    })

#---------------- BUDDY LISTING  ---------------------
def buddy_list_view(request):
    buddies = CustomUser.objects.filter(is_active=True)\
        .exclude(is_staff=True)\
        .exclude(is_superuser=True)\
        .exclude(id=request.user.id)
    return render(request, 'social_app/buddyup.html', {'buddies': buddies})


#---------------- UNFRIEND A BUDDY ---------------------
@login_required
def unfriend_view(request, buddy_id):
    buddy = get_object_or_404(CustomUser, pk=buddy_id) #REMOVE BUDDY
    buddy_req = BuddyRequest.objects.filter( #LOCATE ACCEPTED BUDDY REQUEST
        Q(sender=request.user, receiver=buddy) | Q(sender=buddy, receiver=request.user),
        status='accepted'
    ).first()

    if buddy_req:
        message = buddy_req.unfriend(request.user) #CALL THE UNFRIEND METHOD IN BuddyRequest model
    else:
        request.user.buddies.remove(buddy)# IF NO ACCEPTED BUDDY REQUEST, REMOVE BUDDY
        buddy.buddies.remove(request.user)
        message = f"You are no longer buddies with {buddy.username}."

    request.user.refresh_from_db()  #REFRESH USER DATABASE
    return buddy_profile_view(request, request.user.id, message) #RE-RENDER THE PROFILE PAGE

#---------------- BUDDY LISTING DETAIL (AJAX) ---------------------
def buddy_details_ajax(request, buddy_id):
    try:
        buddy = CustomUser.objects.get(pk=buddy_id)
    except CustomUser.DoesNotExist:
        raise Http404("Buddy not found")
    data = {
        'username': buddy.username,
    }
    return JsonResponse(data)

#---------------- BUDDY-UP REQUEST (AJAX) ---------------------
@login_required
@require_POST
def send_buddy_request_ajax(request):
    buddy_id = request.POST.get('buddy_id')
    if not buddy_id:
        return HttpResponseBadRequest("No buddy_id provided")

    UserModel = get_user_model()
    try:
        receiver = UserModel.objects.get(pk=buddy_id)
    except UserModel.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")

    BuddyRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status': 'pending'}
    )
    return JsonResponse({'message': 'Buddy request sent', 'buddy_id': buddy_id})