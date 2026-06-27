from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Requested'),
        ('ACCEPTED', 'Accepted'),
        ('ON_THE_WAY', 'Mechanic On The Way'),
        ('ARRIVED', 'Arrived'),
        ('REPAIR_STARTED', 'Repair Started'),
        ('REPAIR_COMPLETED', 'Repair Completed'),
        ('PAYMENT_PENDING', 'Payment Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )

    PROBLEM_CHOICES = (
        ('FLAT_TYRE', 'Flat Tyre'),
        ('BATTERY_ISSUE', 'Battery Issue'),
        ('ENGINE_PROBLEM', 'Engine Problem'),
        ('FUEL_DELIVERY', 'Fuel Delivery'),
        ('ACCIDENT', 'Accident'),
        ('LOCKOUT', 'Lockout'),
        ('TOWING', 'Towing'),
        ('GENERAL', 'General Breakdown'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_requests')
    mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_requests', null=True)
    preferred_mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_jobs')
    
    problem_category = models.CharField(max_length=50, choices=PROBLEM_CHOICES, default='GENERAL')
    problem_description = models.TextField()
    emergency_contact = models.CharField(max_length=20)
    
    current_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    current_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request #{self.id} - {self.vehicle.registration_number if self.vehicle else 'No Vehicle'}"

class ServiceImage(models.Model):
    IMAGE_TYPE_CHOICES = (
        ('PROBLEM', 'Problem Image'),
        ('REPAIR_BEFORE', 'Before Repair'),
        ('REPAIR_AFTER', 'After Repair'),
    )
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_images/')
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='PROBLEM')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class RepairDetails(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='repair_details')
    repair_notes = models.TextField(blank=True, null=True)
    parts_used = models.TextField(blank=True, null=True)
    labour_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    parts_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def total_cost(self):
        return self.labour_charges + self.parts_charges

class StatusUpdate(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=ServiceRequest.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
