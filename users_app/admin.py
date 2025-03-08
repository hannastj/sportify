from django.contrib import admin #IZZAK: Gives access to djangos admin panel
from django.contrib.auth.admin import UserAdmin #IZZAK: extends the default django user management in /admin/ 
from .models import CustomUser, Gym, SportsClub 

class CustomUserAdmin(UserAdmin):
    #IZZAK: We need to add our custom fields
    fieldsets = UserAdmin.fieldsets + (("Additional Info", {"fields": ("gym", "clubs", "profile_picture", "age", "bio")}),
    )
    #IZZAK: defines the columns and how we can filter users
    list_display = ("username", "email", "get_gyms", "get_clubs")
    list_filter = ("gym", "clubs")

    #IZZAK: Now we have to have getters. 
    def get_gyms(self, obj):
        return ", ".join([gym.name for gym in obj.gym.all()])

    def get_clubs(self, obj):
        return ", ".join([club.name for club in obj.clubs.all()])

    get_gyms.short_description = "Gyms"
    get_clubs.short_description = "Clubs"

# Registering models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Gym)
admin.site.register(SportsClub)
