from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CusUser

class CusUserChangeForm(UserChangeForm):
    class Meta:
        model = CusUser
        fields = ('email', 'firstname', 'username', 'is_staff')

class CusUserCreationForm(UserCreationForm):
    class Meta:
        model = CusUser
        fields = ('email', 'firstname', 'username', 'password1', 'password2')
