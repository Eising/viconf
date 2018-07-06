from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Template
# Create your views here.

# Templates view

class TemplateList(generic.ListView):
    template_name = "templates/list.djhtml"
    context_object_name = "templates"

    def get_queryset(self):
        return Template.objects.exclude(deleted=True)

class TemplateView(generic.DetailView):
    model = Template
    template_name = "templates/view.djhtml"

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
    def form_valid(self, form):
        super(TemplateCreate, self).form_valid(form)
        templ = self.object
        return HttpResponseRedirect(reverse('configuration:templetags' pk=templ.id))

class TemplateUpdate(UpdateView):
    model = Template
    template_name = "templates/create.djhtml"

class TemplateTags(UpdateView):
    model = Template
    template_name = "templates/tags.djhtml"

class TemplateDelete(DeleteView):
    model = Template
    template_name = "templates/confirm_delete.djhtml"
    sucess_url = reverse_lazy("templates")

def template_clone(request, template_id):
    # Logic to clone templates
    return HttpResponseRedirect(reverse('configuration:templates'))


class ProvisionList(generic.ListView):
    template_name = "provision/provision.djhtml"

class FormList(generic.ListView):
    template_name = "forms/list.djhtml"


# Form views
