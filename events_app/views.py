from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from .models import WorkoutEvent
from .forms import WorkoutEventForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#----------------------- EVENTS PAGE  ----------------------------
@login_required
def events_view(request):
    events = WorkoutEvent.objects.filter(is_public=True)
    return render(request, 'events_app/events.html', {'events': events})

#---------------- EVENT SEARCH FUNCTION ---------------------
@login_required
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

    context = {'events': events, 'q': q, 'search': True}
    return render(request, 'events_app/events.html', context)

#---------------- JOINING OR LEAVING AN EVENT ---------------------
@login_required
@require_POST
def join_event_view(request, event_id):
    event = get_object_or_404(WorkoutEvent, id=event_id)
    event.participants.add(request.user)
    return JsonResponse({'status': 'joined', 'event_id': event.id})

@login_required
@require_POST
def leave_event_view(request, event_id):
    event = get_object_or_404(WorkoutEvent, id=event_id)
    event.participants.remove(request.user)
    return JsonResponse({'status': 'left', 'event_id': event.id})

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
    return render(request, 'events_app/events.html', {
        'events': events,
        'active_tab': 'my'
    })

#---------------- DELETE AN EVENT ---------------------
@login_required
def delete_event_view(request, event_id):
    # Ensure the event exists and belongs to the user
    event = get_object_or_404(WorkoutEvent, id=event_id, host=request.user)
    event.delete()
    return redirect('events_app:my_events')

#---------------- PUBLIC EVENTS ---------------------
@login_required
def public_events_view(request):
    events = WorkoutEvent.objects.filter(is_public=True)
    return render(request, 'events_app/events.html', {
        'events': events,
        'active_tab': 'public'
    })

#---------------- PRIVATE EVENTS ---------------------
@login_required
def private_events_view(request):
    # Return only private events where the host is the logged-in user or one of their buddies
    events = WorkoutEvent.objects.filter(
        is_public=False
    ).filter(
        Q(host=request.user) | Q(host__in=request.user.buddies.all())
    )
    return render(request, 'events_app/events.html', {
        'events': events,
        'active_tab': 'private'
    })