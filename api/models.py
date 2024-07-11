from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(primary_key=True, unique=True, max_length=150)
    first_name = models.CharField(max_length=56)
    last_name = models.CharField(max_length=56)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
