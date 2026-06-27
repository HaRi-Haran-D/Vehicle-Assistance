from django.db.models.signals import post_save
from django.dispatch import receiver
from assistance.models import StatusUpdate
from .models import Notification
from django.urls import reverse

@receiver(post_save, sender=StatusUpdate)
def notify_status_change(sender, instance, created, **kwargs):
    if created:
        request = instance.service_request
        
        # Notify Customer
        Notification.objects.create(
            user=request.customer,
            message=f"Your request #{request.id} status is now: {instance.get_status_display()}",
            link=reverse('request_detail', kwargs={'pk': request.id})
        )
        
        # Notify Mechanic if assigned
        if request.mechanic:
            Notification.objects.create(
                user=request.mechanic,
                message=f"Job #{request.id} status updated to: {instance.get_status_display()}",
                link=reverse('job_detail', kwargs={'pk': request.id}) # Assuming mechanic job detail uses the same or a different view
            )
