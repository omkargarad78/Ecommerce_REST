from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=120)
    address=models.TextField(blank=True)
    phone=models.CharField(max_length=15,blank=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email
    
    