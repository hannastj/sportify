from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from social_app.models import BuddyRequest

User = get_user_model()

#----------------------- Buddy Up View Tests --------------------------

class BuddyViewsTests(TestCase):
    def setUp(self):
        # Create two test users: one to send the request and one to receive it.
        self.sender = User.objects.create_user(
            username='sender', email='sender@example.com', password='pass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver', email='receiver@example.com', password='pass123'
        )

    def test_send_buddy_request(self):
        # Log in as the sender.
        self.client.login(username='sender', password='pass123')
        url = reverse('social_app:send_buddy_request')
        data = {'buddy_id': self.receiver.id}
        response = self.client.post(url, data)
        
        # Check that a BuddyRequest was created.
        buddy_req = BuddyRequest.objects.filter(sender=self.sender, receiver=self.receiver).first()
        self.assertIsNotNone(buddy_req)
        self.assertEqual(buddy_req.status, 'pending')
        
        # Check that the response includes the confirmation message.
        self.assertContains(response, "Buddy request sent")

    def test_buddy_search(self):
        # Create additional users with 'doe' in their username.
        User.objects.create_user(username='john_doe', email='john@example.com', password='pass123')
        User.objects.create_user(username='jane_doe', email='jane@example.com', password='pass123')
        
        # Perform a search for 'doe'.
        url = reverse('social_app:buddy_search')
        response = self.client.get(url, {'q': 'doe'})
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response.
        json_response = response.json()
        self.assertIn('users', json_response)
        
        # Check that each returned username contains the search term 'doe'.
        for user_data in json_response['users']:
            self.assertIn('doe', user_data['username'].lower())
            

#----------------------- Buddy Up Model Tests --------------------------

class BuddyRequestModelTest(TestCase):
    def setUp(self):
        # Create two test users for the buddy request.
        self.sender = User.objects.create_user(
            username='sender', email='sender@example.com', password='pass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver', email='receiver@example.com', password='pass123'
        )
        # Create a buddy request with initial status "pending".
        self.buddy_request = BuddyRequest.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            status='pending'
        )

    def test_accept_method(self):
        # Call the model's accept method.
        self.buddy_request.accept()

        # Refresh the instances from the database to reflect updates.
        self.buddy_request.refresh_from_db()
        self.sender.refresh_from_db()
        self.receiver.refresh_from_db()

        # Assert that the buddy request status has been updated to "accepted".
        self.assertEqual(self.buddy_request.status, 'accepted')
        # Verify that both users have been added to each other's buddy lists.
        self.assertIn(self.receiver, self.sender.buddies.all())
        self.assertIn(self.sender, self.receiver.buddies.all())
