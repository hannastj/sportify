from django.contrib import admin
from django import forms
from django.db import models
from .models import WorkoutEvent

class WorkoutEventAdmin(admin.ModelAdmin):
    # Displays participants as checklist in admin interface
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }

admin.site.register(WorkoutEvent, WorkoutEventAdmin)
