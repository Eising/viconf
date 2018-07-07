from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from util.templatehelpers import abbr_on_template
from util.pystachehelper import get_configurable_tags
from util.validators import ViconfValidators

import re
import sys
import json

from .models import Template
# Create your views here.

# Templates view

class TemplateList(generic.ListView):
    template_name = "templates/list.djhtml"
    context_object_name = "templates"

    def get_queryset(self):
        return Template.objects.exclude(deleted=True)

def template_view(request, pk):
    template = get_object_or_404(Template, pk=pk)
    up_contents =  abbr_on_template(template.up_contents, json.loads(template.fields))
    down_contents = abbr_on_template(template.down_contents, json.loads(template.fields))
    return render(request, 'templates/view.djhtml', {'template': template, 'up_contents': up_contents, 'down_contents': down_contents })



class TemplateCreate(CreateView):
    model = Template
    template_name = "templates/create.djhtml"
    fields = [
        "name",
        "description",
        "platform",
        "up_contents",
        "down_contents"
    ]

    def get_success_url(self):
        templ = self.object
        return reverse_lazy('configuration:templatetags', kwargs={'template_id': templ.id})

class TemplateUpdate(UpdateView):
    model = Template
    template_name = "templates/create.djhtml"
    fields = [
        "name",
        "description",
        "platform",
        "up_contents",
        "down_contents"
    ]
    def get_success_url(self):
        templ = self.object
        return reverse_lazy('configuration:templatetags', kwargs={'template_id': templ.id})



def template_delete(request, pk):
    template = get_object_or_404(Template, pk=pk)
    template.deleted = True
    template.save()
    return HttpResponseRedirect(reverse('configuration:templates'))


def template_clone(request, template_id):
    # Logic to clone templates
    return HttpResponseRedirect(reverse('configuration:templates'))

def template_tags(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    if request.method == 'GET':
        up_template = template.up_contents
        down_template = template.down_contents
        tags = set()
        for tag in get_configurable_tags(up_template):
            tags.add(tag)
        for tag in get_configurable_tags(down_template):
            tags.add(tag)

        validators = ViconfValidators.VALIDATORS
        return render(request, 'templates/tags.djhtml', {'template': template, 'tags': tags, 'validators': validators})
    elif request.method == 'POST':
        tags = dict()
        for key, value in request.POST.items():
            param = re.match(r'^tag\.(\S+)$', key)
            if param is not None:
                tags[param.group(1)] = value
        template.fields = json.dumps(tags)
        template.save()

        return HttpResponseRedirect(reverse('configuration:templates'))



# Form views
