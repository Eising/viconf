from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render

from .models import ConfigTask
from configuration.models import Service

from .tasks import push_to_device_task

# Create your views here.

def configure_device(request, pk, direction):
    service = get_object_or_404(Service, pk=pk)
    if direction == "up":
        config = service.config_set.first().up_config
    elif direction == "down":
        config = service.config_set.first().down_config
    else:
        return HttpResponse(status=400)


    configtask = ConfigTask()
    configtask.config = config
    configtask.service = service
    configtask.state = 'STARTING'
    configtask.save()

    # start task
    task = push_to_device_task.delay(pk=configtask.id, commit=False)

    return HttpResponseRedirect(reverse('tasks:view', kwargs={'pk': configtask.id }))

def confirm_task(request, uuid):
    configtask = get_object_or_404(ConfigTask, pk=uuid)
    if configtask.state != 'READY':
        return HttpResponseRedirect(reverse('tasks:view', kwargs={'pk': configtask.id }))

    task = push_to_device_task.delay(pk=pk, commit=True)
    return HttpResponseRedirect(reverse('tasks:view', kwargs={'pk': configtask.id }))

def view_task(request, pk):
    task = get_object_or_404(ConfigTask, pk=pk)

    return render(request, "view.djhtml", {'task': task})

def json_task(request, pk):
    task = get_object_or_404(ConfigTask, pk=pk)
    data = {'state': task.state, 'diff': task.diff}

    return JsonResponse(data)
