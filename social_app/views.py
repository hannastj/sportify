from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import BuddyRequest

#---------------- SENDING A BUDDY REQUEST ---------------------
def send_buddy_request_view(request, user_id):
    if request.method == 'POST':
        receiver = get_object_or_404(User, pk=user_id)
        BuddyRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver,
            defaults={'status': 'pending'}
        )
    return redirect('profile', user_id=user_id)

#---------------- ACCEPT OR DECLINE BUDDY REQUEST ---------------------
def respond_buddy_request_view(request, request_id):
    if request.method == 'POST':
        buddy_req = get_object_or_404(BuddyRequest, id=request_id, receiver=request.user)
        action = request.POST.get('action')  #USER ENTERS 'ACCEPT' OR 'DECLINE'
        if action == 'accept':
            buddy_req.status = 'accepted'
        elif action == 'reject':
            buddy_req.status = 'rejected'
        buddy_req.save()
    return redirect('buddy_requests_list')

#---------------- PENDING BUDDY REQUESTS ---------------------
def buddy_requests_list_view(request):
    incoming = BuddyRequest.objects.filter(receiver=request.user, status='pending')
    outgoing = BuddyRequest.objects.filter(sender=request.user, status='pending')
    return render(request, 'buddy_requests.html', {'incoming': incoming, 'outgoing': outgoing})


#---------------- BUDDY SEARCH ---------------------
def search_users_view(request):
    query = request.GET.get('q', '')
    if query:
        results = User.objects.filter(username__icontains=query)
    else:
        results = []
    return render(request, 'search_users.html', {'results': results, 'query': query})