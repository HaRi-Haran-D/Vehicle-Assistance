from django.db import models
from django.conf import settings

class MechanicProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mechanic_profile')
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    vehicle_types_supported = models.CharField(max_length=255, help_text="e.g. Car, Bike, Truck", blank=True)
    current_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    documents = models.FileField(upload_to='mechanic_docs/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
