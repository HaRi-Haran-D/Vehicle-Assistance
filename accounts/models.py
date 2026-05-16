from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('MECHANIC', 'Mechanic'),
        ('ADMIN', 'Admin'),
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    def is_customer(self):
        return self.role == 'CUSTOMER'

    def is_mechanic(self):
        return self.role == 'MECHANIC'

    def is_admin(self):
        return self.role == 'ADMIN'
