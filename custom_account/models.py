from django.db import models
from django.contrib.auth.models import User
from yellow_hat.constants import JOB_CHOICES


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_role = models.CharField(
        max_length=100,
        choices=JOB_CHOICES,
        default="other",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username} Profile"
