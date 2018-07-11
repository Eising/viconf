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

    def fetch_inventory_tuple(tag):
        (invname, field, selector) = tag

        parent = Inventory.objects.filter(fields__name=invname).first()

        data = list()

        for inventory in parent.inventory_set.all():
            data.append((inventory.fields[selector], inventory.fields[field]))

        return data

    def fetch_inventory_tuple_with_ids(tag):
        (invname, field, selector) = tag

        parent = Inventory.objects.filter(fields__name=invname).first()

        data = list()

        for inventory in parent.inventory_set.all():
            data.append((selector, inventory.fields[selector], inventory.id))

        return data

    def reverse(inventory, pk):
        parent = Inventory.objects.filter(fields__name=inventory).first()
        structure = parent.fields['fields']

        row = Inventory.objects.get(pk=pk)

        data = dict()
        for key in structure.keys():
            data[key] = row.fields[key]

        return data
