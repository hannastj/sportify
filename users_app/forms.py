from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import CustomUser, Gym, SportsClub

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text="Must be a University of Glasgow Student Email")
    gym = forms.ModelMultipleChoiceField(
        queryset=Gym.objects.all(), 
        widget=forms.CheckboxSelectMultiple(), 
        required=True
    )
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "gym")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        help_texts = password_validation.password_validators_help_texts()
        bullet_list = "<ul>"
        for text in help_texts:
            bullet_list += f"<li>{text}</li>"
        bullet_list += "</ul>"
        self.fields["password1"].help_text = bullet_list
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@student.gla.ac.uk"):
            raise forms.ValidationError("Email must be a University of Glasgow student Email")
        return email

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    clubs = forms.ModelMultipleChoiceField(
        queryset=SportsClub.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False
    )
    gym = forms.ModelMultipleChoiceField(
        queryset=Gym.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=True, 
        help_text="Required."
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': '250', 'id': 'bio'}), 
        required=False
    )
    
    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'first_name', 'last_name', 'age', 'bio', 'clubs', 'gym')
