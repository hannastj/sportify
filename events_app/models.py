from django.db import models
from django.conf import settings

#-------------------WORKOUT EVENTS-------------------------
class WorkoutEvent(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hosted_events")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False) #Events are private by default

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='events_joined', blank=True)

    def __str__(self):
        return self.title
