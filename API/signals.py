from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(signal=post_save, sender=models.Payment)
def set_payment_details(sender, instance, created, **kwargs):
    if created:
        first_name = instance.pupil.first_name
        last_name = instance.pupil.last_name
        group_name = instance.group.name

        instance.first_name = first_name
        instance.last_name = last_name
        instance.group_name = group_name
        instance.save()


