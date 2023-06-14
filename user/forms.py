from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Userprofile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Create a form to login users with email instead of username

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))  
    class Meta:
        model = User
        fields = ['username', 'password']

        # fields = ("old_password","new_password1","new_password2")
        labels = {
            "username":  "E-mail",
        }
        # widgets = {
        #     "password": forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder":"أدخل كلمة المرور الحالية"})
        # }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        # required_fields = ["username", "email", "first_name", "last_name"]

class UpdateProfileForm2(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = ["phone_number", "address"]
        # required_fields = ["phone_number", "address"]
        labels = {
            "phone_number": "Phone Number",
            "address": "Address",
        }
        widgets = {
            "phone_number": forms.TextInput(attrs={'class':'form-control', 'type':'text', "placeholder":"Phone Number"}),
            "address": forms.Textarea(attrs={'class':'form-control', 'type':'text', "placeholder":"Address"}),
        }
        
        
