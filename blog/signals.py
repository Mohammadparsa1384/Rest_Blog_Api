from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment

@receiver(post_save, sender=Comment)
def auto_approved_admin_comment(sender, instance, created, **kwargs):
    if created:
        if instance.author.user.is_staff:
            instance.is_approved = True
            instance.save()