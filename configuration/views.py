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
import copy

from .models import Template, Form, Service, FormForm

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
class FormList(generic.ListView):
    context_object_name = Form
    template_name = "forms/list.djhtml"

    def get_queryset(self):
        return Form.objects.exclude(deleted=True)

    def dispatch(self, request, *args, **kwargs):
        queryset = Form.objects.exclude(deleted=True)

        if not queryset:
            return HttpResponseRedirect(reverse('configuration:formcompose'))
        else:
            return super(FormList, self).dispatch(request, *args, **kwargs)

def form_list(request):
    form = Form.objects.exclude(deleted=True)

    if not form:
        return HttpResponseRedirect(reverse('configuration:formcompose'))
    else:
        return render(request, "forms/list.djhtml", { 'forms': form })

def form_view(request, pk):
    form = get_object_or_404(Form, pk=pk)
    defaults = json.loads(form.defaults)

    return render(request, 'forms/view.djhtml', { 'form': form, 'defaults': defaults})


def form_create(request, pk=None):
    if request.method == 'GET':
        if pk is None:
            formform = FormForm()
            formform.fields['templates'].queryset = Template.objects.exclude(deleted=True)
            return render(request, "forms/compose.djhtml", {'form': formform })
        else:
            form = get_object_or_404(Form, pk=pk)
            name = form.name
            description = form.description
            templates = []
            for template in form.templates:
                templates.add(template)

            templates = ",".join(templates)

            kwargs = {'name': name, 'description': description, 'templates': templates, 'form_id': form.id, 'request': request }

            return HttpResponse(actual_form_create(**kwargs))

    elif request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        templates = request.POST.getlist('templates')

        kwargs = {'name': name, 'description': description, 'templates': templates, 'request': request }
        return HttpResponse(actual_form_create(**kwargs))


def actual_form_create(**kwargs):
    name = kwargs['name']
    description = kwargs['description']
    templates = kwargs['templates']
    request = kwargs['request']

    tags = set()
    for tid in templates:
        up_ctags = get_configurable_tags(Template.objects.get(pk=tid).up_contents)
        down_ctags = get_configurable_tags(Template.objects.get(pk=tid).down_contents)
        for uct in up_ctags:
            tags.add(uct)
        for dct in down_ctags:
            tags.add(uct)

    templates = ",".join(templates)

    if 'form_id' in kwargs:
        form = get_object_or_404(Form, pk=form_id)
        defaults = json.loads(form.defaults)

        return render(request, "forms/config.djhtml", {'name': name, 'description': description, 'tags': tags, 'templates': templates, 'form': form, 'defaults': defaults })
    else:
        return render(request, "forms/config.djhtml", {'name': name, 'description': description, 'tags': tags, 'templates': templates })





def form_config(request):
    if request.method == 'POST':
        defaults = dict()
        for key, value in request.POST.items():
            param = re.match(r'^(default|name)\.(\S+)$', key)
            if param is not None:
                keytype = param.group(1)
                field = param.group(2)
                if not field in defaults:
                    defaults[field] = dict()
                if keytype == 'default':
                    defaults[field]["value"] = value
                elif keytype == 'name':
                    defaults[field]["name"] = value

        defaults = json.dumps(defaults)
        params = copy.deepcopy(request.POST)
        params['defaults'] = defaults
        templates = list()
        for template in params['templates'].split(','):
            print(template, file=sys.stderr)
            templates.append(Template.objects.get(pk=template))

        params['templates'] = templates
        print(params, file=sys.stderr)
        form = Form(name=params['name'], description=params['description'], defaults=defaults)
        form.save()
        for template in templates:
            form.templates.add(template)
        form.save()



        return HttpResponseRedirect(reverse('configuration:forms'))



def form_delete(request, pk):
    form = get_object_or_404(Form, pk=pk)

    form.deleted = True
    form.save()

    return HttpResponseRedirect(reverse('configuration:forms'))



# Generic classes for working urls...

class ProvisionList(generic.ListView):
    context_object_name = Service
