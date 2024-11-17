# Create your models here.
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default-profile.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"