from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='info')

    is_streaming = models.BooleanField(default=False)

    github_profile = models.URLField(null=True, blank=True)
    stackoverflow_profile = models.URLField(null=True, blank=True)
    twitch_channel = models.CharField(max_length=255)


@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)