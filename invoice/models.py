from django.db import models

# Create your models here.
class Trainer(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class college(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
