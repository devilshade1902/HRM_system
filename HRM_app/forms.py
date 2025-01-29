from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HRM_Users

class UserForm(UserCreationForm):
    class Meta:
        model = HRM_Users
        fields = ['fname','lname','email1','password1','password2']