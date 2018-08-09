from django.db import models
from django.contrib.postgres.fields import JSONField
from collections import OrderedDict


# Create your models here.

class Inventory(models.Model):
    fields = JSONField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def _ordered_fields(self):
        ofield = OrderedDict()
        if 'fields' in self.fields:
            for field in self.fields['fields']:
                ofield[field[1]] = field[2]
            return ofield
        else:
            return self.fields
    ordered_fields = property(_ordered_fields)
