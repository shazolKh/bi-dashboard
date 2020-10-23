from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from durationwidget.widgets import TimeDurationWidget

from .models import CustomUser, License


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name")


class LicenseForm(forms.ModelForm):

    duration = forms.DurationField(widget=TimeDurationWidget(), required=False)

    class Meta:
        model = License
        fields = ("license_type", "name", "price", "duration")
