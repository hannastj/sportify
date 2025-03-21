from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

#-------------------WORKOUT EVENTS---------------------------

class WorkoutEvent(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hosted_events")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)  # Events are private by default
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participated_events")

    def clean(self):
        # Ensure that the start time is before the end time
        super().clean() 
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

