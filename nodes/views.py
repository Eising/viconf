from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

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

class GroupDetailView(generic.DetailView):
    model = Group
    template_name = "groups/view.djhtml"
