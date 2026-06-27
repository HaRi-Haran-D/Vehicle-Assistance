from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review

@receiver(post_save, sender=Review)
def update_mechanic_rating(sender, instance, created, **kwargs):
    mechanic = instance.mechanic
    avg_rating = Review.objects.filter(mechanic=mechanic).aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        if hasattr(mechanic, 'mechanic_profile'):
            mechanic.mechanic_profile.rating = round(avg_rating, 2)
            mechanic.mechanic_profile.save()
