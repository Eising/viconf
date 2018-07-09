from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django import forms

from .models import Group, Node

# Create your views here.

class IndexView(generic.ListView):
    template_name = "nodes/index.djhtml"
    context_object_name = 'all_nodes'

    def get_queryset(self):
        return Node.objects.all()

class DetailView(generic.DetailView):
    model = Node
    template_name = "nodes/view.djhtml"

def node_delete(request, node_id):
    node = get_object_or_404(Node, pk=node_id)
    node.delete()
    return HttpResponseRedirect(reverse('nodes:index'))

class GroupView(generic.ListView):
    template_name = "groups/index.djhtml"
    context_object_name = "all_groups"

    def get_queryset(self):
        return Group.objects.all()

class GroupCreateView(CreateView):
    model = Group
    fields = [ 'name', 'username', 'password', 'enable_password' ]
    template_name = "groups/create.djhtml"
    success_url = reverse_lazy('nodes:groups')

    def get_form(self):
        form = super(GroupCreateView, self).get_form()
        form.fields['password'].widget = forms.PasswordInput()
        form.fields['enable_password'].widget = forms.PasswordInput()

        return form

class GroupDetailView(generic.DetailView):
    model = Group
    template_name = "groups/view.djhtml"


class NodeCreateView(CreateView):
    model = Node
    fields = [ 'hostname', 'ipv4', 'ipv6', 'driver', 'comment', 'group' ]
    template_name =  "nodes/create.djhtml"
    success_url = reverse_lazy('nodes:index')
