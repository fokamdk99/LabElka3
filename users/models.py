from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profession = models.CharField(max_length=64)
    znajomi = models.ManyToManyField("self")