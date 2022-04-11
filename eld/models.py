from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cdl_number = models.CharField(max_length=20, blank=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    co_driver_id = models.IntegerField(blank=True, null=True)
    app_version = models.CharField(max_length=5, blank=True)
    notes = models.CharField(max_length=255, blank=True)


class Vehicle(models.Model):
    unit_number = models.CharField(
        max_length=10, primary_key=True, unique=True)
    model = models.CharField(max_length=20, blank=True, null=True)
    vin_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=1)
    notes = models.CharField(max_length=255, blank=True, null=True)


class Log(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    status_code = models.SmallIntegerField(default=0)
    date = models.DateField()
    time = models.TimeField()
    loc_name = models.CharField(max_length=50,  blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    vehicle_id = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, null=True)
    odometer = models.IntegerField(null=True)
    eng_hours = models.DecimalField(max_digits=6, decimal_places=1, null=True)
    notes = models.CharField(max_length=20, blank=True, null=True)
    document = models.CharField(max_length=20,  blank=True, null=True)
    trailer = models.CharField(max_length=20,  blank=True, null=True)


class Location(models.Model):
    loc_name = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
