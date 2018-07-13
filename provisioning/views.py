from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import ConfigTask
from configuration.models import Service

from .tasks import push_to_device_task
# Create your views here.

# Helper function
def configure_service(pk, direction):
    service = get_object_or_404(Service, pk=pk)
    if direction == 'up':
        config = service.config_set.first().up_config
    elif direction == 'down':
        config = service.config_set.first().down_config
    else:
        return HttpResponse(status=400)

    configtask = ConfigTask()
    configtask.config = config
    configtask.service = service
    configtask.state = 'STARTING'
    configtask.save()

    # Start task
    task =  push_to_device_task.delay(pk=configtask.id, commit=False)

    return HttpResponseRedirect(reverse('provisioning:view', kwargs={'pk': configtask.id}))

@login_required
def provision_up(request, pk):
    return configure_service(pk=pk, direction='up')

@login_required
def provision_down(request, pk):
    return configure_service(pk=pk, direction='down')

@login_required
def view_task(request, pk):
    data = {"somedata": "FOOOO"}
    configtask = get_object_or_404(ConfigTask, pk=pk)

    return render(request, "provisioning/view.djhtml", {'configtask': configtask})

    #return JsonResponse(data)

@login_required
def commit_task(request, pk):
    configtask = get_object_or_404(ConfigTask, pk=pk)
    # Actual logic here
    configtask.state = 'STARTING'
    configtask.save()
    task = push_to_device_task.delay(pk=configtask.id, commit=True)


    return HttpResponseRedirect(reverse('provisioning:view', kwargs={'pk': configtask.id}))
