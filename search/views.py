from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from configuration.models import Template, Form, Service
from inventory.models import Inventory
from nodes.models import Node
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def search(request):
    # Assume that this is some sort of JSON request with query as 'query'

    query = request.GET.get('query')
    templates = Template.objects.exclude(deleted=True).filter(name__icontains=query)[:10]
    forms = Form.objects.exclude(deleted=True).filter(name__icontains=query)[:10]
    services = Service.objects.exclude(deleted=True).filter(reference__icontains=query)[:10]

    nodes = Node.objects.filter(hostname__icontains=query)[:10]

    results = len(templates) + len(forms) + len(services) + len(nodes)

    return render(request, "results.djhtml", {'results': results,
                                              'templates': templates,
                                              'forms': forms,
                                              'services': services,
                                              'nodes': nodes})
