from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    CHOICES = (
        ("TP", "Transpoter"),
        ("AD", "Administrator"),
    )

    acc_type = models.CharField(max_length=40, choices=CHOICES)
    acc_status = models.BooleanField(default=True)