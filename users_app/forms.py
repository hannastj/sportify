from django import forms #IZZAK: Added
from django.contrib.auth.forms import UserCreationForm # IZZAK: This is built into django
from .models import CustomUser, Gym, SportsClub #IZZAK: Added

class RegistrationForm(UserCreationForm):
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
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "gym") #Username has been removed currently
        # IZZAK: username uniquenss is automatically enforced in Django's authentication system

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # HS: Pull in the help text from all active validators
            help_texts = password_validation.password_validators_help_texts()

            # HS: Create a bullet list of requirement messages
            bullet_list = "<ul>"
            for text in help_texts:
                bullet_list += f"<li>{text}</li>"
            bullet_list += "</ul>"

            # HS: Assign the bullet list to the password1 field's help_text
            self.fields["password1"].help_text = bullet_list

        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@student.gla.ac.uk"):
        # IZZAK: This is the equivalent of throwing an excpetion in java
            raise forms.ValidationError("Email must be a University of Glasgow student Email")
        return email
    
class ProfileUpdateForm(forms.ModelForm): 
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")

    clubs = forms.ModelMultipleChoiceField(queryset=SportsClub.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    
    gym = forms.ModelMultipleChoiceField(queryset=Gym.objects.all(), widget=forms.CheckboxSelectMultiple, required=True, help_text="Required.")

    bio = forms.CharField(widget=forms.Textarea(attrs={'maxlength': '250', 'id': 'bio' }), required=False)

    background_photo = forms.ImageField(required=False, help_text="Optional: Upload a background photo")

    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'background_photo', 'age', 'bio', 'clubs', 'gym', 'first_name', 'last_name')