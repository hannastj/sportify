import io
from PIL import Image
from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from users_app.models import Gym, SportsClub

User = get_user_model()


#----------------------- Login Page Tests --------------------------

class UserLoginTests(TestCase):

    def setUp(self):
        # Create a Gym instance that is one of the allowed options.
        self.gym = Gym.objects.create(name="Stevenson Building")

        self.test_password = 'ComplexPassword123'
        self.user = User.objects.create_user(
            username='testuser',
            email='2461029f@student.gla.ac.uk',
            password=self.test_password,
        )


    def test_user_signup_creates_custom_user(self):
        # Record the initial number of users
        initial_user_count = User.objects.count()

        # Prepare signup data
        signup_data = {
            'register': 'true',
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser2',
            'email': '2461029f@student.gla.ac.uk',
            'password1': 'ComplexPassword123',
            'password2': 'ComplexPassword123',
            'gym': [self.gym.pk],
        }

        # Simulate a POST request to your signup view
        response = self.client.post(reverse('login'), signup_data)

        # Check that a new user has been created.
        self.assertEqual(User.objects.count(), initial_user_count + 1)

        # Fetch and verify the new user's attributes.
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)

    def test_user_can_login(self):
        # Prepare login data using the credentials from setUp.
        login_data = {
            'login': 'true',  # Hidden field to indicate a login form submission
            'username': 'testuser',
            'password': self.test_password,
        }

        # Simulate a POST request to the login view.
        response = self.client.post(reverse('login'), login_data, follow=True)

        # Check if the user is authenticated.
        self.assertTrue(response.context['user'].is_authenticated)
        # Check the response status code.
        self.assertEqual(response.status_code, 200)


#----------------------- Home Page/ Nav Bar  --------------------------

class NavBarViewTests(TestCase):

    def test_navbar_contains_correct_links(self):
        # Request a page that extends base.html (e.g., home view)
        response = self.client.get(reverse('users_app:home'))

        # Check that the base template nav bar items are in the response.
        self.assertContains(response, 'Sportify')  # Navbar brand
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Buddy-Up')
        self.assertContains(response, 'Events')
        self.assertContains(response, 'Logout')

        # Optionally, you can also check if the links point to the correct URLs.
        self.assertContains(response, reverse('users_app:home'))
        self.assertContains(response, reverse('users_app:profile'))
        self.assertContains(response, reverse('social_app:buddyup'))
        self.assertContains(response, reverse('events_app:public_events'))
        self.assertContains(response, reverse('users_app:logout'))


#----------------------- Profile Edit Page/ Profile Page  --------------------------

def generate_test_image():
    # Create a 1x1 red pixel image
    file = io.BytesIO()
    image = Image.new("RGB", (1, 1), (255, 0, 0))
    image.save(file, 'JPEG')
    file.seek(0)
    return file.read()

class EditProfileTest(TestCase):
    def setUp(self):
        # Create test instances for Gym and SportsClub, needed for the form.
        self.gym = Gym.objects.create(name="Test Gym")
        self.club = SportsClub.objects.create(name="Test Club")
        self.test_password = 'ComplexPassword123'
        
        # Create a test user with initial data.
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password=self.test_password,
            first_name="Test",
            last_name="User",
            age=25,
            bio="Old bio"
        )
        
        # Log in the test user.
        self.client.login(username='testuser', password=self.test_password)

    def test_profile_update(self):
        # Generate a valid image file.
        image_data = generate_test_image()
        image = SimpleUploadedFile("test_image.jpg", image_data, content_type="image/jpeg")
        
        # Prepare updated profile data.
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'age': 30,
            'bio': 'New bio content goes here.',
            'gym': [self.gym.pk],
            'clubs': [self.club.pk],
            'profile_picture': image,
        }
        
        # Submit a POST request to the edit profile view.
        response = self.client.post(reverse('edit_profile'), updated_data, follow=True)
        
        # Assert that the user is redirected to the profile page after saving.
        self.assertRedirects(response, reverse('profile'))
        
        # Refresh the user instance from the database.
        self.user.refresh_from_db()
        
        # Verify that the user’s attributes have been updated.
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.age, 30)
        self.assertEqual(self.user.bio, 'New bio content goes here.')
        
        # Check that many-to-many relationships have been updated.
        self.assertIn(self.gym, self.user.gym.all())
        self.assertIn(self.club, self.user.clubs.all())
        
        # Check that the profile_picture field was updated.
        self.assertTrue(self.user.profile_picture)
        self.assertIn("test_image.jpg", self.user.profile_picture.name)
        
#----------------------- Logout  --------------------------
class UserLogoutTests(TestCase):

    def setUp(self):
        self.test_password = 'ComplexPassword123'
        self.user = User.objects.create_user(
            username='testuser',
            email='2461029f@student.gla.ac.uk',
            password=self.test_password,
        )

    def test_user_logout(self):
        # Log in the user
        login_successful = self.client.login(username='testuser', password=self.test_password)
        self.assertTrue(login_successful)

        # Simulate a request to the logout view. Adjust the method (GET/POST) as per your logout view.
        response = self.client.get(reverse('users_app:logout'), follow=True)

        # Check that the user is logged out
        self.assertFalse(response.context['user'].is_authenticated)