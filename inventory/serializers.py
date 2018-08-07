from rest_framework import serializers
from inventory.helpers.helpers import InventoryHelpers


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    parent_id = serializers.IntegerField(read_only=True)
    fields = serializers.JSONField()

    def create(self, validated_data):
        #        print(validated_data, file=sys.stderr)
        parent = validated_data['parent']
        data = validated_data['fields']
        return InventoryHelpers.add_inventory_row(parent, data)


"""
        if parent_id is not None:
            # We are creating a row on an inventory
            # Check exists?
            parent = Inventory.objects.get(pk=parent)
            row = InventoryHelpers.add_inventory_row(parent, validated_data)
"""
