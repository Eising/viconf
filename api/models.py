import uuid
from django.db import models

# Create your models here.

class ConfigRequest(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   target = models.CharField(max_length=255)
   config = models.TextField()

class StatusMessage(models.Model):
   request = models.ForeignKey(ConfigRequest, on_delete=models.SET_NULL, null=True)
   response = models.TextField(blank=True)
   status = models.CharField(max_length=255)
