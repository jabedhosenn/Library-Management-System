from django import forms
from .models import Review,Borrow
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from typing import Any

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['body','rating']


class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']