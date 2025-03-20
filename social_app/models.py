from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from users_app.models import CustomUser


#-------------------BUDDY REQUEST---------------------------
class BuddyRequest(models.Model):
    # Users can be a...
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)

    # Status of buddy request
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver') # User can’t send multiple requests to the same person

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"
    
        # HANNA new method: When a request is accepted, users are added as buddies
    def accept(self):
        # Mark the request as accepted and update both users' buddy lists
        self.status = 'accepted'
        self.save()
        # Add each other as buddies
        self.sender.buddies.add(self.receiver)
        self.receiver.buddies.add(self.sender)

    def decline(self):
        self.status = 'rejected'
        self.save()

    def unfriend(self, user_id):
        current_user = self.user
        buddy = get_object_or_404(CustomUser, pk=user_id)

        # Remove each other from the buddy lists
        current_user.buddies.remove(buddy)
        buddy.buddies.remove(current_user)
        message = f"You are no longer buddies with {buddy.username}."
        return redirect('buddy_list')