from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

UserModel = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address.",
        widget=forms.EmailInput(attrs={"placeholder": "Email address"}),
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Username",
            "password1": "Password",
            "password2": "Confirm password",
        }
        help_texts = {
            "username": "Choose a unique username.",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(disabled=True, required=False)
    email = forms.EmailField(disabled=True, required=False)

    class Meta:
        model = Profile
        fields = ("profile_picture", "bio", "city")
        labels = {
            "profile_picture": "Profile picture",
            "bio": "Short bio",
            "city": "City",
        }
        help_texts = {
            "bio": "Tell others a little about yourself.",
            "city": "Optional.",
        }
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write a short introduction...",
                }
            ),
            "city": forms.TextInput(
                attrs={"placeholder": "Your city"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["username"].initial = user.username
            self.fields["email"].initial = user.email