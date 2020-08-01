# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Driver(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False, unique=True,
                              validators=[RegexValidator(r'^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')])
    phone_number = models.CharField(unique=True, max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    license_number = models.CharField(max_length=30, unique=True, null=False)
    car_number = models.CharField(max_length=10, unique=True, null=False)

    class Meta:
        managed = True
        db_table = "driver"


class DriverLocation(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING)
    longitude = models.FloatField(null=False, unique=False)
    latitude = models.FloatField(null=False, unique=False)

    class Meta:
        managed = True
        db_table = "driver_location"
