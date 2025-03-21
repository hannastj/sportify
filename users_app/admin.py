from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Gym, SportsClub 

class CustomUserAdmin(UserAdmin):
    #Add our custom fields
    fieldsets = UserAdmin.fieldsets + (("Additional Info", {"fields": ("gym", "clubs", "profile_picture", "age", "bio")}),
    )
    #Define the columns and how we can filter users
    list_display = ("username", "email", "get_gyms", "get_clubs")
    list_filter = ("gym", "clubs")

    def get_gyms(self, obj):
        return ", ".join([gym.name for gym in obj.gym.all()])

    def get_clubs(self, obj):
        return ", ".join([club.name for club in obj.clubs.all()])

    get_gyms.short_description = "Gyms"
    get_clubs.short_description = "Clubs"

#Registering models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Gym)
admin.site.register(SportsClub)
