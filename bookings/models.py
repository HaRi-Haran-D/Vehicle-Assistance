from django.db import models
from django.conf import settings

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Requested'),
        ('ACCEPTED', 'Accepted'),
        ('ON_THE_WAY', 'On The Way'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_requests')
    mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    issue_type = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    user_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    user_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    mechanic_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    mechanic_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.id} - {self.issue_type} ({self.status})"

class Review(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.mechanic.username} by {self.user.username}"
