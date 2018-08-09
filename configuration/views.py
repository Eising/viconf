from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from util.templatehelpers import abbr_on_template
from util.pystachehelper import get_configurable_tags, PystacheHelpers
from util.validators import ViconfValidators
from inventory.helpers.helpers import InventoryHelpers

import re
import copy
import pystache

from .models import Template, Form, Service, FormForm, Config, Link
from nodes.models import Node
from inventory.models import Inventory

# Templates view


class TemplateList(LoginRequiredMixin, generic.ListView):
    template_name = "templates/list.djhtml"
    context_object_name = "templates"

    def get_queryset(self):
        return Template.objects.exclude(deleted=True)


class TemplateListDeleted(LoginRequiredMixin, generic.ListView):
    template_name = "templates/list.djhtml"
    context_object_name = "templates"

    def get_queryset(self):
        return Template.objects.filter(deleted=True)

    def get_context_data(self, **kwargs):
        context = super(TemplateListDeleted, self).get_context_data(**kwargs)
        context['undelete'] = True

        return context


@login_required
def template_view(request, pk):
    template = get_object_or_404(Template, pk=pk)
    up_contents = abbr_on_template(template.up_contents, template.fields)
    down_contents = abbr_on_template(template.down_contents, template.fields)
    return render(request, 'templates/view.djhtml', {
        'template': template,
        'up_contents': up_contents,
        'down_contents': down_contents
    })


class TemplateCreate(LoginRequiredMixin, CreateView):
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
        return reverse_lazy('configuration:templatetags',
                            kwargs={'template_id': templ.id})

    def get_context_data(self, **kwargs):
        context = super(TemplateCreate, self).get_context_data(**kwargs)
        context['inventories'] = Inventory.objects.exclude(
            deleted=True).filter(parent__isnull=True)

        return context


class TemplateUpdate(LoginRequiredMixin, UpdateView):
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
        return reverse_lazy('configuration:templatetags',
                            kwargs={'template_id': templ.id})


@login_required
def template_delete(request, pk):
    template = get_object_or_404(Template, pk=pk)
    template.deleted = True
    template.save()
    return HttpResponseRedirect(reverse('configuration:templates'))


@login_required
def template_undelete(request, pk):
    template = get_object_or_404(Template, pk=pk)
    template.deleted = False
    template.save()
    return HttpResponseRedirect(reverse('configuration:templates'))


@login_required
def template_tags(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    # Mark all associated forms as require update
    for form in template.form_set.all():
        form.require_update = True
        form.save()

    if request.method == 'GET':
        up_template = template.up_contents
        down_template = template.down_contents
        tags = set()
        for tag in get_configurable_tags(up_template):
            tags.add(tag)
        for tag in get_configurable_tags(down_template):
            tags.add(tag)

        validators = ViconfValidators.VALIDATORS
        return render(request, 'templates/tags.djhtml',
                      {'template': template,
                       'tags': tags,
                       'validators': validators})
    elif request.method == 'POST':
        tags = dict()
        for key, value in request.POST.items():
            param = re.match(r'^tag\.(\S+)$', key)
            if param is not None:
                tags[param.group(1)] = value
        template.fields = tags
        template.save()

        return HttpResponseRedirect(reverse('configuration:templates'))


# Form views

@login_required
def form_list(request):
    form = Form.objects.exclude(deleted=True)

    if not form:
        return HttpResponseRedirect(reverse('configuration:formcompose'))
    else:
        return render(request, "forms/list.djhtml", {'forms': form})


def form_list_deleted(request):
    form = Form.objects.filter(deleted=True)

    if not form:
        return HttpResponseRedirect(reverse('configuration:formcompose'))
    else:
        return render(request, "forms/list.djhtml",
                      {'forms': form, 'undelete': True})


@login_required
def form_view(request, pk):
    form = get_object_or_404(Form, pk=pk)
    defaults = form.defaults

    return render(request, 'forms/view.djhtml',
                  {'form': form, 'defaults': defaults})


@login_required
def form_create(request, pk=None):
    if request.method == 'GET':
        if pk is None:
            formform = FormForm()
            formform.fields['templates'].queryset = Template.objects.exclude(
                deleted=True)
            return render(request, "forms/compose.djhtml", {'form': formform})
        else:
            form = get_object_or_404(Form, pk=pk)
            name = form.name
            description = form.description
            templates = []
            for template in form.templates.all():
                templates.append(str(template.id))

#            templates = ",".join(templates)

            kwargs = {'name': name, 'description': description,
                      'templates': templates, 'form_id': form.id,
                      'request': request}

            return HttpResponse(actual_form_create(**kwargs))

    elif request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        templates = request.POST.getlist('templates')

        kwargs = {'name': name, 'description': description,
                  'templates': templates, 'request': request}
        return HttpResponse(actual_form_create(**kwargs))


def actual_form_create(**kwargs):
    pt = PystacheHelpers()
    name = kwargs['name']
    description = kwargs['description']
    templates = kwargs['templates']
    request = kwargs['request']

    tags = set()
    for tid in templates:

        up_ctags = pt.parse_template_tags(
            Template.objects.get(pk=tid).up_contents)['user_tags']
        down_ctags = pt.parse_template_tags(
            Template.objects.get(pk=tid).down_contents)['user_tags']
        for uct in up_ctags:
            tags.add(uct)
        for dct in down_ctags:
            tags.add(uct)

    templates = ",".join(templates)

    defaults = dict()

    if 'form_id' in kwargs:
        form_id = kwargs['form_id']
        form = get_object_or_404(Form, pk=form_id)
        tdefaults = form.defaults
        for tag in tags:
            if tag in tdefaults:
                defaults[tag] = {'name': tdefaults[tag]
                                 ['name'], 'value': tdefaults[tag]['value']}
            else:
                defaults[tag] = {'name': '', 'value': ''}
        return render(request,
                      "forms/config.djhtml",
                      {'name': name, 'description': description,
                       'tags': tags, 'templates': templates, 'form': form,
                       'defaults': defaults})
    else:
        for tag in tags:
            defaults[tag] = {'name': '', 'value': ''}

        return render(request, "forms/config.djhtml",
                      {'name': name, 'description': description, 'tags': tags,
                       'templates': templates, 'defaults': defaults})


@login_required
def form_config(request):
    if request.method == 'POST':
        defaults = dict()
        for key, value in request.POST.items():
            param = re.match(r'^(default|name)\.(\S+)$', key)
            if param is not None:
                keytype = param.group(1)
                field = param.group(2)
                if field not in defaults:
                    defaults[field] = dict()
                if keytype == 'default':
                    defaults[field]["value"] = value
                elif keytype == 'name':
                    defaults[field]["name"] = value

        defaults = defaults
        params = copy.deepcopy(request.POST)
        params['defaults'] = defaults
        templates = list()
        for template in params['templates'].split(','):
            templates.append(Template.objects.get(pk=template))

        params['templates'] = templates
        if request.POST.get('form_id'):
            form_id = request.POST.get('form_id')
            form = Form.objects.get(pk=form_id)
            form.defaults = defaults
            form.require_update = False
        else:
            form = Form(
                name=params['name'], description=params['description'],
                defaults=defaults)
        form.save()
        for template in templates:
            form.templates.add(template)
        form.save()

        return HttpResponseRedirect(reverse('configuration:forms'))


@login_required
def form_delete(request, pk):
    form = get_object_or_404(Form, pk=pk)

    form.deleted = True
    form.save()

    return HttpResponseRedirect(reverse('configuration:forms'))


@login_required
def form_undelete(request, pk):
    form = get_object_or_404(Form, pk=pk)

    form.deleted = False
    form.save()

    return HttpResponseRedirect(reverse('configuration:forms'))

# Service Provisioning


@login_required
def service_provision(request):
    form = Form.objects.exclude(deleted=True).exclude(require_update=True)
    if request.method == 'GET':
        products = Service.objects.exclude(
            deleted=True, product__isnull=True).distinct('product')
        nodes = Node.objects.all()
        dynurl = reverse('configuration:servicedynamic',
                         kwargs={'pk': 0}).rstrip("/0")
        return render(request, "services/provision.djhtml", {'forms': form, 'nodes': nodes, 'products': products, 'dynurl': dynurl})
    elif request.method == 'POST':
        # Process the submitted
        link_node_id = request.POST.get('link_node_id', None)
        params = {
            'reference': request.POST.get('reference'),
            'customer': request.POST.get('customer', ''),
            'location': request.POST.get('location', ''),
            'product': request.POST.get('product', ''),
            'form_id': request.POST.get('form_id'),
            'comment': request.POST.get('comment', ''),
        }

        template_fields = dict()
        for key, value in request.POST.items():
            param = re.match(r'^form\.(\S+)$', key)
            listparam = re.match(r'^formlist\.(\S+)$', key)
            if param is not None:
                field = param.group(1)
                template_fields[field] = value
            if listparam is not None:
                field = listparam.group(1)
                template_fields[field] = value.split(",")

        inventories = dict()
        for key, value in request.POST.items():
            param = re.match(r'^inv\.(.*)$', key)
            if param is not None:
                inventories[param.group(1)] = value

        template_fields['inventories'] = inventories

        if link_node_id:
            link_node = Node.objects.get(pk=link_node_id)
            template_fields['_link_hostname'] = link_node.hostname
            template_fields['_link_ipv4'] = link_node.ipv4
            template_fields['_link_ipv6'] = link_node.ipv6

        params['template_fields'] = template_fields
        node = Node.objects.get(pk=request.POST.get('node'))
        form = Form.objects.get(pk=request.POST.get('form_id'))
        params['node'] = node
        params['form'] = form

        service = Service(reference=params['reference'], customer=params['customer'], location=params['location'],
                          product=params['product'], template_fields=params['template_fields'],
                          node=params['node'], form=params['form'])
        service.save()

        if link_node_id:
            link = Link(service=service)
            link.save()
            link.node.add(node, link_node)
        else:
            link = Link(service=service)
            link.save()
            link.node.add(node)

        return HttpResponseRedirect(reverse('configuration:renderservice', kwargs={'service_id': service.id}))


@login_required
def service_dynamic(request, pk):
    form = Form.objects.get(pk=pk)
    defaults = dict()
    all_tags = set()
    all_fields = dict()
    all_lists = set()
    link_tags = set()
    inventory_tags = set()
    nodes = Node.objects.all()
    pt = PystacheHelpers()
    for template in form.templates.all():
        up_template_tags = pt.parse_template_tags(template.up_contents)
        down_template_tags = pt.parse_template_tags(template.down_contents)
        for tag in up_template_tags['user_tags']:
            all_tags.add(tag)
        for tag in down_template_tags['user_tags']:
            all_tags.add(tag)
        for tag in up_template_tags['link_tags']:
            link_tags.add(tag)
        for tag in down_template_tags['link_tags']:
            link_tags.add(tag)
        for tag in up_template_tags['inventory_tags']:
            inventory_tags.add(tag)
        for tag in down_template_tags['inventory_tags']:
            inventory_tags.add(tag)
        for tag in up_template_tags['list_tags']:
            all_lists.add(tag)
        for tag in down_template_tags['list_tags']:
            all_lists.add(tag)

        fields = template.fields
        for field, klass in fields.items():
            if field not in all_fields:
                all_fields[field] = klass

    defaults = form.defaults
    validators = ViconfValidators.VALIDATORS

    for tag in all_tags:
        if tag in defaults:
            if all_fields[tag] != 'none':
                defaults[tag]["css_class"] = validators[all_fields[tag]]["css_class"]

    form_inventory = dict()
    for tag in inventory_tags:
        parsed_tag = tag.split("__")
        if len(parsed_tag) == 3:
            form_inventory[parsed_tag[0]] = InventoryHelpers.fetch_inventory_tuple_with_ids(
                parsed_tag)

    return render(request, "services/dynamic.djhtml",
                  {'defaults': defaults, 'link_tags': link_tags,
                   'nodes': nodes, 'inventories': form_inventory,
                   'all_lists': all_lists})


def validate_reference(request):
    reference = request.GET.get('reference', None)
    if Service.objects.exclude(deleted=True).filter(reference__iexact=reference):
        return JsonResponse("reference in use", safe=False)
    else:
        return JsonResponse("true", safe=False)


class ServiceIndex(LoginRequiredMixin, generic.ListView):
    template_name = "services/index.djhtml"
    context_object_name = "all_services"

    def get_queryset(self):
        return Service.objects.exclude(deleted=True)


class ServiceDeletedIndex(LoginRequiredMixin, generic.ListView):
    template_name = "services/index.djhtml"
    context_object_name = "all_services"

    def get_queryset(self):
        return Service.objects.filter(deleted=True)

    def get_context_data(self, **kwargs):
        context = super(ServiceDeletedIndex, self).get_context_data(**kwargs)
        context['undelete'] = True

        return context


@login_required
def service_config(request, pk):
    service = get_object_or_404(Service, pk=pk)
    config = get_object_or_404(Config, service=service)

    return HttpResponseRedirect(reverse('configuration:configview', kwargs={'pk': config.id}))

# Config


@login_required
def render_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    pt = PystacheHelpers()

    params = service.template_fields
    params['reference'] = service.reference
    params['customer'] = service.customer
    params['location'] = service.location
    params['node'] = service.node
    invdata = dict()
    invtags = set()
    up_template = []
    down_template = []

    for inventoryname, inventoryid in service.template_fields['inventories'].items():
        keyprefix = "_i_{}".format(inventoryname)
        for column, value in InventoryHelpers.reverse(inventoryname, inventoryid).items():
            keyname = "{}__{}".format(keyprefix, column)
            invdata[keyname] = value

    # Collect inventory tags
    for template in service.form.templates.all():
        for tag in pt.parse_template_tags(template.up_contents)['inventory_tags']:
            invtags.add("_i_" + tag)

    for tag in invtags:
        lookup = tag.rsplit("__", 1)[0]  # Remove the selector
        if lookup in invdata:
            params[tag] = invdata[lookup]

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
        config = Config(up_config=up_template,
                        down_config=down_template, service=service)

    config.save()
    return HttpResponseRedirect(reverse('configuration:configview', kwargs={'pk': config.id}))


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)

    service.deleted = True

    service.save()

    return HttpResponseRedirect(reverse('configuration:services'))


def service_undelete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if len(Service.objects.exclude(deleted=True)
           .filter(reference__iexact=service.reference)) > 0:
        return render(request, "services/refcollision.djhtml")
    else:

        service.deleted = False

        service.save()

        return HttpResponseRedirect(reverse('configuration:services'))


@login_required
def config_view(request, pk):
    config = get_object_or_404(Config, pk=pk)

    return render(request, "config/view.djhtml", {'config': config})


# validators

def validatorjs(request):
    validators = ViconfValidators.VALIDATORS

    return render(request, "js/validators.js", {'validators': validators})

# Generic classes for working urls...
