from django.db import models

# Create your models here.

class formmodel(models.Model):
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    email = models.CharField()
    message = models.TextField()
    