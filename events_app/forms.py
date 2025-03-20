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

    # This creates a checkbox for the boolean field.
    is_public = forms.BooleanField(
        label="Make event public?",
        required=False,  # Not required means unchecked (False) is acceptable.
        initial=False   # Defaults to False, meaning the event is private by default.
    )

    class Meta:
        model = WorkoutEvent
        fields = [
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
            'is_public',
        ]

    def clean_description(self):
        
        description = self.cleaned_data.get('description', '')
        word_limit = 50
        words = description.split()

        if len(words) > word_limit:
            raise forms.ValidationError(f"Description cannot exceed {word_limit} words.")
        return description
