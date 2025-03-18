from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import WorkoutEvent
from .forms import WorkoutEventForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#----------------------- EVENTS PAGE  ----------------------------
def events_view(request):
    return render(request, 'events_app/events.html')

#---------------- EVENT SEARCH FILTER ---------------------
def search_events_view(request):
    q = request.GET.get('q', '')
    if q:
        events = WorkoutEvent.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(host__username__icontains=q)
        ).distinct()
    else:
        events = WorkoutEvent.objects.none()
    # Optionally, you can add a context variable to indicate a search is active.
    context = {'events': events, 'q': q, 'search': True}
    return render(request, 'events_app/events.html', context)

#---------------- JOINING OR LEAVING AN EVENT ---------------------
def join_event_view(request, event_id):
    event = get_object_or_404(WorkoutEvent, id=event_id)
    event.participants.add(request.user)
    return redirect('event_detail', event_id=event.id)

def leave_event_view(request, event_id):
    event = get_object_or_404(WorkoutEvent, id=event_id)
    event.participants.remove(request.user)
    return redirect('event_detail', event_id=event.id)

#---------------- BROWSING AN EVENT ---------------------
from django.utils import timezone

def event_feed_view(request):
    now = timezone.now()
    events = WorkoutEvent.objects.filter(start_time__gte=now).order_by('start_time')
    return render(request, 'events_app/event_feed.html')

#---------------- CREATING AN EVENT ---------------------
@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = WorkoutEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            # Clear any existing participants, then add the creator
            event.participants.clear()
            event.participants.add(request.user)
            return redirect('events_app:events')
    else:
        form = WorkoutEventForm()
    return render(request, 'events_app/create_event.html', {'form': form})


#---------------- MY EVENTS ---------------------
@login_required
def my_events_view(request):
    # Get events where the user is the host or a participant
    hosted_events = WorkoutEvent.objects.filter(host=request.user)
    participated_events = WorkoutEvent.objects.filter(participants=request.user)
    # Combine the two querysets and remove duplicates
    events = (hosted_events | participated_events).distinct()
    
    context = {'events': events}
    return render(request, 'events_app/events.html', context)

#---------------- DELETE AN EVENT ---------------------
@login_required
def delete_event_view(request, event_id):
    # Ensure the event exists and belongs to the user
    event = get_object_or_404(WorkoutEvent, id=event_id, host=request.user)
    event.delete()
    return redirect('events_app:my_events')

#---------------- PUBLIC EVENTS ---------------------
def public_events_view(request):
    events = WorkoutEvent.objects.filter(is_public=True)
    return render(request, 'events_app/events.html', {
        'events': events,
        'active_tab': 'public'
    })

#---------------- PRIVATE EVENTS ---------------------
def private_events_view(request):
    events = WorkoutEvent.objects.filter(is_public=False)
    return render(request, 'events_app/events.html', {
        'events': events,
        'active_tab': 'private'
    })