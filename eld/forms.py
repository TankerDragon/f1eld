from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Driver, Vehicle


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class DriverDetailForm(ModelForm):
    class Meta:
        model = Driver
        # ['user_id', 'cdl_number', 'vehicle_id', 'notes']
        fields = ['cdl_number', 'vehicle_id',
                  'co_driver_id', 'notes', 'user']


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
