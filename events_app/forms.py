from django import forms
from .models import WorkoutEvent

class WorkoutEventForm(forms.ModelForm):
    class Meta:
        model = WorkoutEvent
        fields = [
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
            'participants',
        ]
