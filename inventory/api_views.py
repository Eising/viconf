from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Inventory

from .serializers import InventorySerializer


def api_view_inventories(request):
    inventories = Inventory.objects.exclude(
        deleted=True).filter(parent__isnull=True)
    serializer = InventorySerializer(inventories, many=True)

    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def api_get_inventory_by_name(request, name):
    if request.method == 'GET':
        inventory_query = Inventory.objects.filter(fields__name=name).first()
        if not inventory_query:
            return(Http404)
        else:
            return api_show_inventory(inventory_query)
    elif request.method == 'POST':
        inventory_query = Inventory.objects.filter(fields__name=name).first()
        if not inventory_query:
            return(Http404)
        else:
            parent = inventory_query
            data = JSONParser().parse(request)
            return api_add_row(parent, data)


@csrf_exempt
def api_get_inventory_by_id(request, pk):
    if request.method == 'GET':
        inventory = get_object_or_404(Inventory, pk=pk)
        return api_show_inventory(inventory)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        parent = get_object_or_404(Inventory, pk=pk)
        return api_add_row(parent, data)


def api_show_inventory(inventory):
    children = Inventory.objects.filter(parent=inventory)
    serializer = InventorySerializer(children, many=True)

    return JsonResponse(serializer.data, safe=False)


def api_add_row(parent, data):
    serializer = InventorySerializer(data=data)
    if serializer.is_valid():
        serializer.save(parent=parent)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


def api_show_row(row_id):
    inventory = Inventory.objects.get(pk=row_id)
    serializer = InventorySerializer(inventory)

    return JsonResponse(serializer.data, safe=False)


def api_get_inventory_row_by_name(request, name, rowid):
    # The inventory name is just for sanity checking here
    inventory_query = Inventory.objects.filter(fields__name=name).first()
    if not inventory_query:
        raise Http404("Inventory not found")
    else:
        # check if rowid is child of inventory
        parent = inventory_query
        row = get_object_or_404(Inventory, pk=rowid)
        if row.parent != parent:
            raise Http404("Parent mismatch")
        else:
            return api_show_row(rowid)


def api_get_inventory_row_by_id(request, pk, rowid):
    inventory = get_object_or_404(Inventory, pk=pk)
    row = get_object_or_404(Inventory, pk=rowid)

    if row.parent != inventory:
        raise Http404("Parent mismatch")
    else:
        return api_show_row(rowid)
