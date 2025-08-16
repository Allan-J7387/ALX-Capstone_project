from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("CITIZEN","Citizen"),
        ("DISPATCHER","Dispatcher"),
        ("DRIVER","Driver"),
        ("ADMIN","Admin"),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="CITIZEN")
