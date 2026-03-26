from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CountryCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    country_name = models.CharField(max_length=100)
    country_flag = models.ImageField(upload_to='country_flags/', blank=True, null=True)

    def __str__(self):
        return f"{self.country_name} ({self.code})"

class User(AbstractUser):
    # allready existing fields in AbstractUser:
    # username, first_name, last_name, email, password, is_staff, is_superuser, groups, permissions
    country_code = models.ForeignKey(
        CountryCode,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.username