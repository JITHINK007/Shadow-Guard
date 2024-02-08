from django.db import models
from django.db import connections
from django import forms

class Signup(models.Model):
    USERNAME = models.CharField(max_length=50)
    PASSWORD = models.CharField(max_length=50)
    EMAIL = models.EmailField()
    class Meta:
        db_table="login"

class Detect(models.Model):
    ID=models.IntegerField()
    DATE=models.CharField(max_length=100)
    TIME=models.CharField(max_length=100)
    LOCATION=models.CharField(max_length=100)
    WEAPON=models.CharField(max_length=100)
    SENT_TO=models.CharField(max_length=100)
    IMAGE=models.ImageField()

    class Meta:
        db_table="detect"



