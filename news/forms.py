from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": " "
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": " "
        })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "input",
                "placeholder": " "
            }),
            "first_name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": " "
            }),
            "last_name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": " "
            }),
        }


class SignInForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "input-container",
        "placeholder": "Enter email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "input-container",
        "placeholder": "Enter password"
    }))

    class Meta:
        model = User
        fields = ['email', 'password']
