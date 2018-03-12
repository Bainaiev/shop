import os

from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from . import models


@receiver(post_delete, sender=models.Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Product` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=models.Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Product` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = models.Product.objects.get(pk=instance.pk).image
    except models.Product.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# @receiver(post_save, sender=models.User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         models.User.objects.create(user=instance)
#     instance.profile.save()            