from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from util.validators import ViconfValidators


from inventory.helpers.helpers import InventoryHelpers

from .models import Inventory

import re

# Create your views here.

def view_inventories(request):

    inventories = Inventory.objects.exclude(deleted=True).filter(parent__isnull=True)
    return render(request, 'index.djhtml', {'inventories': inventories })


def add_inventory(request):

    if request.method == 'GET':
        validators = ViconfValidators.VALIDATORS
        return render(request, 'create.djhtml', {'validators': validators})


    elif request.method == 'POST':
        # Something
        fields = dict()
        for key, value in request.POST.items():
           param = re.match(r'^field\.(.*)$', key)
           if param is not None:
               fields[param.group(1)] = value


        kwargs = {'name': request.POST.get('name', None), 'fields': fields}
        inventory = InventoryHelpers.add_inventory(**kwargs)

        return HttpResponseRedirect(reverse('inventory:index'))


def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    inventory.deleted = True

    inventory.save()

    return HttpResponseRedirect(reverse('inventory:index'))

def delete_inventory_row(request, pk, row_id):
    inventory = get_object_or_404(Inventory, pk=row_id)
    parent = get_object_or_404(Inventory, pk=pk)
    inventory.delete()

    return HttpResponseRedirect(reverse('inventory:viewinventory', kwargs={ 'pk': pk }))




def view_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    columns = inventory.fields['fields'].keys()
    if request.method == 'GET':
        children = Inventory.objects.filter(parent=inventory)
        return render(request, 'view.djhtml', {'inventory': inventory, 'columns': columns, 'children': children})



def add_row(request, pk):
    if request.method == 'POST':
        inventory = get_object_or_404(Inventory, pk=pk)
        # Add row
        entries = dict()
        for key, value in request.POST.items():
            param = re.match(r'^key\.(.*)$', key)
            if param is not None:
                entries[param.group(1)] = value

        row = InventoryHelpers.add_inventory_row(inventory, entries)

        return HttpResponseRedirect(reverse('inventory:viewinventory', kwargs={'pk': pk}))


def update_row(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        inventory = get_object_or_404(Inventory, pk=pk)
        fields = inventory.fields
        name = request.POST.get('name')
        value = request.POST.get('value')
        fields[name] = value
        inventory.fields = fields
        inventory.save()

        message = {'message': "Sucessfully updated", 'params': fields}
        return JsonResponse(message)
