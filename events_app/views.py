from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import WorkoutEvent
from .forms import WorkoutEventForm

#----------------------- EVENTS PAGE  ----------------------------
def events_view(request):
    return render(request, 'events_app/events.html')

#---------------- EVENT SEARCH FILTER ---------------------
def search_events_view(request):
    q = request.GET.get('q', '')
    if q:
        events = WorkoutEvent.objects.filter(title__icontains=q)
    else:
        events = WorkoutEvent.objects.none()
    return render(request, 'events_app/search_events.html', {'events': events, 'q': q})

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
    return render(request, 'events_app/event_feed.html', {'events': events})

#---------------- CREATING AN EVENT ---------------------
def create_event_view(request):
    if request.method == 'POST':
        form = WorkoutEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = WorkoutEventForm()
    return render(request, 'events_app/create_event.html', {'form': form})