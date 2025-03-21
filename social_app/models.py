from django.db import models
from django.conf import settings

#-------------------BUDDY REQUEST---------------------------
class BuddyRequest(models.Model):
    #USERS CAN BE A SENDER/RECEIVER AND HAVE AN ID
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)

    #REQUESTS STATUS CAN BE THE FOLLOWING, WITH ' PENDING ' SET TO DEFAULT
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    #USERS CAN'T SEND MULTIPLE REQUESTS TO THE SAME PERSON
    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"
    
    #WHEN A REQUEST IS ACCEPTED, USERS ARE ADDED TO EACH OTHER'S BUDDY LIST
    def accept(self):
        self.status = 'accepted'
        self.save()
        self.sender.buddies.add(self.receiver)
        self.receiver.buddies.add(self.sender)

    #IF REJECTED, NOTHING HAPPENS
    def decline(self):
        self.status = 'rejected'
        self.save()

    #UNFRIEND METHOD
    def unfriend(self, current_user):

        #FIND OUT WHICH USER IS THE BUDDY
        if current_user == self.sender:
            buddy = self.receiver
        elif current_user == self.receiver:
            buddy = self.sender
        else:
            raise ValueError("Current user is not associated with this buddy request.")

        #REMOVE
        current_user.buddies.remove(buddy)
        buddy.buddies.remove(current_user)

        #CLEAN UP ANY PRIOR ACCEPTED BUDDY REQUEST FROM THESE TWO USERS
        BuddyRequest.objects.filter(sender=current_user, receiver=buddy, status='accepted').delete()
        BuddyRequest.objects.filter(sender=buddy, receiver=current_user, status='accepted').delete()

        return f"You are no longer buddies with {buddy.username}."