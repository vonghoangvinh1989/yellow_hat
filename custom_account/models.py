from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )  # related_name='profile' is helpful for easy reverse relation from User to Profile
    job_role = models.CharField(max_length=50, blank=True, null=True, default="Other")

    def __str__(self):
        return self.user.username if self.user else "No User"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # When the user is created, we create the profile and set the job_role
        Profile.objects.create(user=instance, job_role="Other")
    else:
        # If the user exists, we simply save the profile (no need to update job_role)
        instance.profile.save()
