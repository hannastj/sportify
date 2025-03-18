from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,get_object_or_404,render
from django.contrib.auth.models import User
from social_app import models
from social_app.models import BuddyRequest
from users_app.models import CustomUser
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST


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