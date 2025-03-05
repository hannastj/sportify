from django.core.management.base import BaseCommand
from users_app.models import Gym, SportsClub

class Command(BaseCommand):
    help = 'Populates the database with preset Gym and SportsClub entries'

    def handle(self, *args, **options):
        # Define the preset gyms
        gym_names = ["Stevenson Building", "Garscube Sports Complex"]
        
        # Define the preset sports clubs
        sports_clubs = [
            "American Football", "Athletics", "Badminton", "Basketball", "Boat Club",
            "Boxing", "Canoeing", "Caving", "Cheerleading", "Cricket", "Curling",
            "Cycling", "Fencing", "Football", "Gaelic Football", "Golf", "Gymnastics",
            "Handball", "Hares & Hounds", "Hockey", "Judo", "Karate", "Kendo", "Lacrosse",
            "Mountaineering", "Muay Thai", "Netball", "Riding", "Rugby", "Running", "Sailing",
            "Shinty", "Shorinji Kempo", "Skiing", "Skydiving", "Snowboarding", "Squash", "Surfing",
            "Swimming", "Table Tennis", "Taekwondo", "Tennis", "Trampoline", "Triathlon",
            "Ultimate Frisbee", "Volleyball", "Wakeboarding", "Water Polo", "Weightlifting", "Yoga"
        ]

        # Populate gyms
        for gym_name in gym_names:
            gym, created = Gym.objects.get_or_create(name=gym_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Gym: {gym.name}"))
            else:
                self.stdout.write(f"Gym already exists: {gym.name}")

        # Populate sports clubs
        for club_name in sports_clubs:
            club, created = SportsClub.objects.get_or_create(name=club_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created SportsClub: {club.name}"))
            else:
                self.stdout.write(f"SportsClub already exists: {club.name}")

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
