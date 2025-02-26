from django.db import models
from django.contrib.auth.models import User

#-------------------WORKOUT EVENTS-------------------------
class WorkoutEvent(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(User, related_name='events_joined', blank=True)

    def __str__(self):
        return self.title
