from django.db import models
from django.contrib.auth.admin import User
# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    is_SO = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_delete, sender=UserProfile)
def userProfile_deleted(sender, instance, *args, **kwargs):
    instance.user.delete()
