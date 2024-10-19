from django.db import models
from django.conf import settings


# Create your models here.
class PenetrationTest(models.Model):
    # Penetration Testing Team Contact Information
    team_primary_contact = models.CharField(max_length=100)
    team_primary_phone = models.CharField(max_length=20)
    team_primary_pager = models.CharField(max_length=20, blank=True, null=True)
    team_secondary_contact = models.CharField(max_length=100, blank=True, null=True)
    team_secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    team_secondary_pager = models.CharField(max_length=20, blank=True, null=True)

    # Target Organization Contact Information
    target_primary_contact = models.CharField(max_length=100)
    target_primary_phone = models.CharField(max_length=20)
    target_primary_pager = models.CharField(max_length=20, blank=True, null=True)
    target_secondary_contact = models.CharField(max_length=100, blank=True, null=True)
    target_secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    target_secondary_pager = models.CharField(max_length=20, blank=True, null=True)

    # Testing Information
    debrief_frequency = models.CharField(max_length=100)
    debrief_location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    test_times = models.CharField(max_length=100)
    announced_test = models.CharField(max_length=10)
    shun_ip = models.CharField(max_length=10)
    automatic_shun = models.TextField()
    shun_steps = models.TextField()
    conclude_test = models.CharField(max_length=10)
    continue_test = models.TextField(blank=True, null=True)
    attack_ips = models.TextField()
    black_box = models.CharField(max_length=10)
    viewing_policy = models.TextField()
    observing_team = models.CharField(max_length=10)

    # Signatures
    target_signature = models.CharField(max_length=100)
    target_date = models.DateField()
    pen_test_leader = models.CharField(max_length=100)
    leader_date = models.DateField()
    tester_signatures = models.TextField(blank=True, null=True)

    target_signature_image = models.ImageField(
        upload_to="signatures/",  # Use settings for dynamic path
        blank=True,
        null=True,
    )
    pen_test_leader_signature_image = models.ImageField(
        upload_to="signatures/",  # Use settings for dynamic path
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Penetration Test from {self.start_date} to {self.end_date}"
