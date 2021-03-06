from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from util.validators import ViconfValidators

from collections import OrderedDict

from django.contrib.auth.decorators import login_required

import django_excel as excel

from inventory.helpers.helpers import InventoryHelpers

from .models import Inventory

from django import forms
from util.validators import ViconfFormValidator

import re

# Create your views here.


@login_required
def view_inventories(request):

    inventories = Inventory.objects.exclude(
        deleted=True).filter(parent__isnull=True)
    return render(request, 'inventory/index.djhtml',
                  {'inventories': inventories})


@login_required
def add_inventory(request):

    if request.method == 'GET':
        validators = ViconfValidators.VALIDATORS
        return render(request, 'inventory/create.djhtml',
                      {'validators': validators})

    elif request.method == 'POST':
        # Something
        fields = list()
        for key, value in request.POST.items():
            param = re.match(r'^field_(\d+)\.(.*)$', key)
            if param is not None:
                index = int(param.group(1))
                field = param.group(2)
                fields.append([index, field, value])

        fields.sort(key=lambda x: x[0])

        kwargs = {'name': request.POST.get('name', None), 'fields': fields}
        InventoryHelpers.add_inventory(**kwargs)

        return HttpResponseRedirect(reverse('inventory:index'))


@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    inventory.deleted = True

    inventory.save()

    return HttpResponseRedirect(reverse('inventory:index'))


@login_required
def delete_inventory_row(request, pk, row_id):
    inventory = get_object_or_404(Inventory, pk=row_id)
    get_object_or_404(Inventory, pk=pk)  # rewrite this
    inventory.delete()

    return HttpResponseRedirect(reverse('inventory:viewinventory',
                                        kwargs={'pk': pk}))


def generate_form(dictionary):
    form_fields = OrderedDict()
    for key, validator in dictionary.items():
        form_fields[key] = forms.CharField(
            validators=[ViconfFormValidator(validator)])

    return type(str('DictionaryGeneratedForm'), (forms.Form,), form_fields)


@login_required
def view_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    columns = inventory.ordered_fields

    InvForm = generate_form(columns)
    form = InvForm()
    if request.method == 'GET':
        children = Inventory.objects.filter(parent=inventory)
        return render(request, 'inventory/view.djhtml',
                      {'inventory': inventory,
                       'form': form,
                       'columns': columns,
                       'children': children})


@login_required
def add_row(request, pk):
    if request.method == 'POST':
        inventory = get_object_or_404(Inventory, pk=pk)
        # Add row
        fieldset = inventory.ordered_fields
        InvForm = generate_form(fieldset)
        form = InvForm(request.POST)
        if form.is_valid():
            InventoryHelpers.add_inventory_row(inventory, form.cleaned_data)

            return HttpResponseRedirect(reverse('inventory:viewinventory',
                                                kwargs={'pk': pk}))
        else:
            children = Inventory.objects.filter(parent=inventory)
            return render(request, 'inventory/view.djhtml',
                          {'inventory': inventory,
                           'form': form,
                           'columns': fieldset,
                           'children': children})


@login_required
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


@login_required
def generate_template(request, pk, export=False):
    inventory = get_object_or_404(Inventory, pk=pk)

    fields = [inventory.ordered_fields.keys()]

    return excel.make_response_from_array(fields, 'xlsx',
                                          file_name="{}.xlsx".format(
                                              inventory.fields['name']))


@login_required
def upload_template(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == 'GET':
        return render(request, 'inventory/upload.djhtml')
    elif request.method == 'POST':

        data = request.FILES['file'].get_records()
        for row in data:
            InventoryHelpers.add_inventory_row(
                parent=inventory, entries=dict(row))

        return HttpResponseRedirect(reverse('inventory:viewinventory',
                                            kwargs={'pk': pk}))
