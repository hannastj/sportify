from django import forms
from .models import WorkoutEvent

# Specifying date/time widget
class WorkoutEventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        }),
        label='Start Time'
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        }),
        label='End Time'
    )

    class Meta:
        model = WorkoutEvent
        fields = [
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
        ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        # Ensuring end_time is after start_time
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data
