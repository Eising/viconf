from django.db import models
from nodes.models import Node
from configuration.models import Service
import uuid

# Create your models here.

class ConfigTask(models.Model):
    STATES = (
        ('STARTING', 'Starting up'),
        ('COMMUNICATING', 'Communiticating with device'),
        ('READY', 'Ready for commit'),
        ('DONE', 'Configuration Committed'),
        ('FAIL', 'Configuration Failed')
    )
    config = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=255, choices=STATES)
    diff = models.TextField(null=True)
