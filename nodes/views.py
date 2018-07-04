from django.http import HttpResponse
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
