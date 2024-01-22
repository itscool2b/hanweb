from django.db import models

# Create your models here.

class formmodel(models.Model):
    firstname = models.CharField(max_length=1000,null=False)
    lastname = models.CharField(max_length=1000,null=False)
    email = models.CharField(max_length=100,null=False)
    message = models.TextField(max_length=1000,null=False)
    
