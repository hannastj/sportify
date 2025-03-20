from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.contrib.auth import get_user_model
from events_app.models import WorkoutEvent

User = get_user_model()

#-------------------EVENT MODEL TESTS---------------------------
class WorkoutEventModelTests(TestCase):
    def setUp(self):
        # Create a host and a participant user for testing
        self.host = User.objects.create_user(username="hostuser", password="password")
        self.participant = User.objects.create_user(username="participant", password="password")

    def test_time_order_validation(self):
        """
        Test that the model enforces start_time to be before end_time.
        """
        # Setting start_time after end_time to trigger validation
        start = timezone.now() + timedelta(hours=2)
        end = timezone.now() + timedelta(hours=1)
        event = WorkoutEvent(
            host=self.host,
            title="Invalid Time Event",
            description="End time is before start time.",
            location="Test Location",
            start_time=start,
            end_time=end,
        )

        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_default_is_public(self):
        """
        Test that the is_public field defaults to False.
        """
        event = WorkoutEvent.objects.create(
            host=self.host,
            title="Default Values Event",
            description="Testing default is_public field.",
            location="Test Location",
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2),
        )
        self.assertFalse(event.is_public)

    def test_add_participants(self):
        """
        Test the many-to-many relationship for participants.
        """
        event = WorkoutEvent.objects.create(
            host=self.host,
            title="Group Event",
            description="Testing adding participants.",
            location="Test Location",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=3),
        )
        # Initially there should be no participants
        self.assertEqual(event.participants.count(), 0)
        # Add a participant and check that they are included
        event.participants.add(self.participant)
        self.assertEqual(event.participants.count(), 1)
        self.assertIn(self.participant, event.participants.all())

#-------------------EVENT VIEW TESTS---------------------------
class WorkoutEventViewTests(TestCase):
    def setUp(self):
        # Create a host user for testing
        self.host = User.objects.create_user(username="hostuser", password="password")

    def test_main_view_with_no_events(self):
        """
        When no workout events exist, the view should display a message indicating that there are no events.
        """
        response = self.client.get(reverse('events_app:events'))
        self.assertEqual(response.status_code, 200)
        # Check for the expected message in the rendered HTML
        self.assertContains(response, "No events found.")
        # Verify that the context variable 'events' is an empty list
        self.assertQuerysetEqual(response.context['events'], [])

    def test_main_view_with_events(self):
        """
        When workout events exist, the view should display them.
        """
        # Create sample workout events
        event1 = WorkoutEvent.objects.create(
            host=self.host,
            title="Morning Run",
            description="A quick morning run in the park.",
            location="Central Park",
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2),
            is_public=True 
        )
        event2 = WorkoutEvent.objects.create(
            host=self.host,
            title="Evening Yoga",
            description="A relaxing yoga session.",
            location="Yoga Studio",
            start_time=timezone.now() + timedelta(hours=3),
            end_time=timezone.now() + timedelta(hours=4),
            is_public=True 
        )
        response = self.client.get(reverse('events_app:events'))
        self.assertEqual(response.status_code, 200)
        # Check that the titles of the created events are contained in the response
        self.assertContains(response, event1.title)
        self.assertContains(response, event2.title)
        # Confirm that the context variable 'events' has exactly 2 items
        self.assertEqual(len(response.context['events']), 2)

