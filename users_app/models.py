from django.db import models
from django.contrib.auth.models import AbstractUser #IZZAK: This is provided by django and provides lots basic attributres we use for users
                                                    #IZZAK: AbstractUser inherits the User class and is used to add Additional Fields required for your User in Database itself
        
#-------------------User Model-----------------    
#IZZAK: Gym choices for users to select

# IZZAK: Gym Model
class Gym(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# IZZAK: Sports Club Model
class SportsClub(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name   
 
# IZZAK: Attributes of each user     
class CustomUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False) 
    gym = models.ManyToManyField(Gym, blank=False)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    clubs = models.ManyToManyField(SportsClub, blank=True)
    
    def __str__(self):
        return self.username
    

#model in the back end must be made




     #["American Football", "Athletics", "Badminton", "Basketball", "Boat Club", "Boxing", "Canoeing", "Caving", "Cheerleading", "Cricket", "Curling", "Cycling", "Fencing", "Football", "Gaelic Football", "Golf", "Gymnastics", "Handball", "Hares & Hounds", "Hockey", "Judo", "Karate", "Kendo", "Lacrosse", "Mountaineering", "Muay Thai", "Netball", "Riding", "Rugby", "Running", "Sailing", "Shinty", "Shorinji Kempo", "Skiing", "Skydiving", "Snowboarding", "Squash", "Surfing", "Swimming", "Table Tennis", "Taekwondo", "Tennis", "Trampoline", "Triathlon", "Ultimate Frisbee", "Volleyball", "Wakeboarding", "Water Polo", Weightlifting", "Yoga"]
