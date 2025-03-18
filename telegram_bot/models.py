from django.db import models


class Refuel(models.Model):
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE) #FK for useraccount
    date = models.DateTimeField() # users input date
    fuel_amount = models.FloatField() #Amount of fuel in gallons
    start_fuel = models.FloatField() # Start fuel
    remaining_fuel = models.FloatField() # Remaining fuel
    start_odometer_reading = models.FloatField() # Start odometer readings
    end_odometer_reading = models.FloatField()  # End odometer readings
    location = models.CharField(max_length=255, blank=True, null=True)# Location
    date_upload = models.DateTimeField(auto_now_add=True) # Date upload


class MPGCalculation(models.Model):
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    date = models.DateTimeField()  # users input date
    fuel_amount = models.FloatField()  # Amount of fuel in gallons
    start_fuel = models.FloatField()  # Start fuel
    remaining_fuel = models.FloatField()  # Remaining fuel
    start_odometer_reading = models.FloatField()  # Start odometer readings
    end_odometer_reading = models.FloatField()  # End odometer readings
    location = models.CharField(max_length=255, blank=True, null=True)  # Location
    distance = models.IntegerField()  # Distance on mile
    fuel_used = models.FloatField()  # Amount of fuel
    mpg = models.FloatField() #result of mpg calculation
    date_upload = models.DateTimeField(auto_now_add=True)


class UserAccount(models.Model):
    telegram_id = models.BigIntegerField(unique=True)  #getting telegram user id
    username = models.CharField(max_length=150, blank=True, null=True)  #getting from telegram username