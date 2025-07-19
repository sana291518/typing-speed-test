from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Performance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, default='')
    typed_text = models.TextField(max_length=500, default='')
    wpm = models.FloatField(default=0)
    accuracy = models.FloatField(default=0.0)
    date = models.DateTimeField(default=timezone.now)
