from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    PROVIDER = 'provider'
    CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (PROVIDER, 'Service Provider'),
        (CUSTOMER, 'Customer'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.username