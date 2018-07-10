from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Inventory(models.Model):
    fields = JSONField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    deleted = models.BooleanField(default=False)
