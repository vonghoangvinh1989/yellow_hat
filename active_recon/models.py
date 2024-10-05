from django.db import models


# Create your models here.
class ActiveReconTool(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def _str__(self):
        return f"{self.name} - {self.description}"