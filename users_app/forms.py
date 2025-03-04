from django import forms #IZZAK: Added
from django.contrib.auth.forms import UserCreationForm # IZZAK: This is built into django
from .models import CustomUser, Gym #IZZAK: Added

class registrationForm(UserCreationForm):
    # IZZAK: We create an email field to say the potential users we only accept UofG student emails
    email = forms.EmailField(help_text="Must be a University of Glasgow Student Email")
    
    # IZZAK: This adds the drop in feature to make sure selecting a gym is mandatory
    gym = forms.ModelMultipleChoiceField(queryset=Gym.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    
    # IZZAK: These are not included in the UserCreationForms
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    
    class Meta:
        # IZZAK: This is a configuration class for CustomUserForm
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "gym")
        # IZZAK: username uniquenss is automatically enforced in Django's authentication system
        
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@student.gla.ac.uk"):
        # IZZAK: This is the equivalent of throwing an excpetion in java
            raise forms.ValidationError("Email must be a University of Glasgow student Email")
        return email