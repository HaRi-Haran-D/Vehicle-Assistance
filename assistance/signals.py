from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import ServiceRequest, StatusUpdate

@receiver(pre_save, sender=ServiceRequest)
def track_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = ServiceRequest.objects.get(pk=instance.pk)
        instance._old_status = old_instance.status
    else:
        instance._old_status = None

@receiver(post_save, sender=ServiceRequest)
def create_status_update(sender, instance, created, **kwargs):
    if created or (hasattr(instance, '_old_status') and instance._old_status != instance.status):
        StatusUpdate.objects.create(
            service_request=instance,
            status=instance.status
        )
