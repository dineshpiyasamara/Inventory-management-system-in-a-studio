from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from system.forms import *


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
