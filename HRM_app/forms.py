from django import forms
from .models import HRM_Users

class UserForm(forms.ModelForm):
    class Meta:
        model = HRM_Users
        fields = ['role', 'description']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = HRM_Users
        fields = ['role', 'description']
    
    