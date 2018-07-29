from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Group, Node, Site

# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "nodes/index.djhtml"
    context_object_name = 'all_nodes'

    def get_queryset(self):
        return Node.objects.all()

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Node
    template_name = "nodes/view.djhtml"

def node_delete(request, node_id):
    node = get_object_or_404(Node, pk=node_id)
    node.delete()
    return HttpResponseRedirect(reverse('nodes:index'))

class GroupView(LoginRequiredMixin, generic.ListView):
    template_name = "groups/index.djhtml"
    context_object_name = "all_groups"

    def get_queryset(self):
        return Group.objects.all()

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = [ 'name', 'username', 'password', 'enable_password' ]
    template_name = "groups/create.djhtml"
    success_url = reverse_lazy('nodes:groups')

    def get_form(self):
        form = super(GroupCreateView, self).get_form()
        form.fields['password'].widget = forms.PasswordInput()
        form.fields['enable_password'].widget = forms.PasswordInput()

        return form

class GroupDetailView(LoginRequiredMixin, generic.DetailView):
    model = Group
    template_name = "groups/view.djhtml"


class NodeCreateView(LoginRequiredMixin, CreateView):
    model = Node
    fields = [ 'hostname', 'ipv4', 'ipv6', 'driver', 'comment', 'group', 'site' ]
    template_name =  "nodes/create.djhtml"
    success_url = reverse_lazy('nodes:index')

class SiteView(LoginRequiredMixin, generic.ListView):
    template_name = "sites/index.djhtml"
    context_object_name = "all_sites"

    def get_queryset(self):
        return Site.objects.all()

class SiteCreateView(LoginRequiredMixin, CreateView):
    model = Site
    fields = [ 'name', 'address', 'latitude', 'longitude', 'comment' ]
    template_name = "sites/create.djhtml"
    success_url = reverse_lazy('nodes:sites')

class SiteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Site
    template_name = "sites/view.djhtml"

def site_delete(request, pk):
    site = get_object_or_404(Site, pk=pk)
    site.delete()
    return HttpResponseRedirect(reverse('nodes:sites'))
