from django.db import models


class Refuel(models.Model):
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    date = models.DateTimeField() 
    fuel_amount = models.FloatField()  # Количество топлива в галлонах
    odometer_reading = models.FloatField()  # Показания одометра
    location = models.CharField(max_length=255, blank=True, null=True)
    date_upload = models.DateTimeField(auto_now_add=True) # Местоположение


class MPGCalculation(models.Model):
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    refuel_start = models.ForeignKey(Refuel, related_name='start_refuel', on_delete=models.CASCADE)
    refuel_end = models.ForeignKey(Refuel, related_name='end_refuel', on_delete=models.CASCADE)
    distance = models.IntegerField()  # Пройденное расстояние в милях
    fuel_used = models.FloatField()  # Количество топлива
    mpg = models.FloatField()


class UserAccount(models.Model):
    telegram_id = models.BigIntegerField(unique=True)  #getting telegram user id
    username = models.CharField(max_length=150, blank=True, null=True)  #getting from telegram username