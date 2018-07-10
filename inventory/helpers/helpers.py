from inventory.models import Inventory
from django.core.exceptions import ValidationError
from util.validators import ViconfValidators
import json

class InventoryHelpers:

    def add_inventory(**kwargs):
        name = kwargs.get('name', None)
        fields = kwargs.get('fields', None)

        if name is None:
            raise ValidationError("name must be set")

        if fields is None:
            raise ValidationError("fields must be set")

        entries = { 'name': name, 'fields': fields }

        inventory = Inventory()
        inventory.fields = entries
        inventory.save()

        return inventory

    def add_inventory_row(parent, entries):
        validators = ViconfValidators()

        fieldset = parent.fields['fields']
        for field, value in entries.items():
            if field not in fieldset:
                raise ValidationError("{} not defined in parent".format(field))
            else:
                validator = fieldset[field]
                if not validators.validate(validator, value):
                    raise ValidationError(validators.VALIDATORS[validator]['error'])
        inventory = Inventory(parent=parent, fields=entries)
        inventory.save()
        return inventory
