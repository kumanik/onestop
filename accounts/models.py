from django.db import models
from django.contrib.auth.models import User
import hashlib


class api_key(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apiKey = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.apiKey = hashlib.sha256(b"{user.username}").hexdigest()
        super(api_key, self).save(*args, **kwargs)
