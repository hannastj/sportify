from django.db import models
from django.contrib.auth.models import User

#-------------------BUDDY REQUEST---------------------------
class BuddyRequest(models.Model):
    #Users can be a...
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)

    #method to show user status
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    #method so user can’t send multiple requests to the same person
    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"