from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
import pystache

from .models import Template, Form, Service, FormForm, Config
from nodes.models import Node

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


# Service Provisioning

def service_provision(request):
    form = Form.objects.exclude(deleted=True)
    if request.method == 'GET':
        products = Service.objects.exclude(deleted=True, product__isnull=True).distinct('product')
        nodes = Node.objects.all()
        dynurl = reverse('configuration:servicedynamic', kwargs={'pk': 0}).rstrip("/0")
        return render(request, "services/provision.djhtml", {'forms': form, 'nodes': nodes, 'products': products, 'dynurl': dynurl })
    elif request.method == 'POST':
        # Process the submitted
        params = {
            'reference': request.POST.get('reference'),
            'customer': request.POST.get('customer', ''),
            'location': request.POST.get('location', ''),
            'product': request.POST.get('product', ''),
            'form_id': request.POST.get('form_id'),
            'comment': request.POST.get('comment', '')
        }

        template_fields = dict()
        for key, value in request.POST.items():
            param = re.match(r'^form\.(\S+)$', key)
            if param is not None:
                field = param.group(1)
                template_fields[field] = value


        params['template_fields'] = json.dumps(template_fields)
        node = Node.objects.get(pk=request.POST.get('node'))
        form = Form.objects.get(pk=request.POST.get('form_id'))
        params['node'] = node
        params['form'] = form

        service = Service(reference=params['reference'], customer=params['customer'], location=params['location'], product=params['product'], template_fields=params['template_fields'], node=params['node'], form=params['form'])
        service.save()

        return HttpResponseRedirect(reverse('configuration:renderservice', kwargs={'service_id': service.id }))



def service_dynamic(request, pk):
    form = Form.objects.get(pk=pk)
    defaults = dict()
    all_tags = set()
    all_fields = dict()
    for template in form.templates.all():
        for tag in get_configurable_tags(template.up_contents):
            all_tags.add(tag)
        for tag in get_configurable_tags(template.down_contents):
            all_tags.add(tag)
        fields = json.loads(template.fields)
        for field, klass in fields.items():
            if field not in all_fields:
                all_fields[field] = klass

    defaults = json.loads(form.defaults)
    validators = ViconfValidators.VALIDATORS

    for tag in all_tags:
        if tag in defaults:
            if all_fields[tag] != 'none':
                defaults[tag]["css_class"] = validators[all_fields[tag]]["css_class"]

    return render(request, "services/dynamic.djhtml", { 'defaults': defaults })

def validate_reference(request):
    reference = request.GET.get('reference', None)
    if Service.objects.filter(reference__iexact=reference):
        return JsonResponse("reference in use", safe=False)
    else:
        return JsonResponse("true", safe=False)


class ServiceIndex(generic.ListView):
    template_name = "services/index.djhtml"
    context_object_name = "all_services"

    def get_queryset(self):
        return Service.objects.exclude(deleted=True)

def service_config(request, pk):
    service = get_object_or_404(Service, pk=pk)
    config = get_object_or_404(Config, service=service)

    return HttpResponseRedirect(reverse('configuration:configview', kwargs={'pk': config.id}))

# Config

def render_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    params = json.loads(service.template_fields)
    params['customer'] = service.customer
    params['location'] = service.location
    params['reference'] = service.reference
    up_template = []
    down_template = []

    for template in service.form.templates.all():
        up_template.append(pystache.render(template.up_contents, params))
        down_template.append(pystache.render(template.down_contents, params))

    up_template = "\n".join(up_template)
    down_template = "\n".join(down_template)

    existing_config = Config.objects.filter(service=service)

    if existing_config:
        config = Config.objects.get(service=service)
        config.up_config = up_template
        config.down_config = down_template
    else:
        config = Config(up_config=up_template, down_config=down_template, service=service)

    config.save()
    return HttpResponseRedirect(reverse('configuration:configview', kwargs={'pk': config.id}))


def config_view(request, pk):
    config = get_object_or_404(Config, pk=pk)

    return render(request, "config/view.djhtml", { 'config': config })



# validators

def validatorjs(request):
    validators = ViconfValidators.VALIDATORS

    return render(request, "js/validators.js", { 'validators': validators })

# Generic classes for working urls...
