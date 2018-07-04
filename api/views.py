from django.shortcuts import render
from django.http import Http404
from rest_framework import generics
from util.napalmhelper import NapalmHelper
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import sys

from nodes.models import Group, Node
from .models import ConfigRequest, StatusMessage

from api.serializers import ConfigSerializer

# Create your views here.

class ConfigRequestList(generics.ListCreateAPIView):
    queryset = ConfigRequest.objects.all()
    serializer_class = ConfigSerializer

    def create(self, request, *args, **kwargs):
        # Let's do some more with the data
        print(request.data, file=sys.stderr)
        target = request.data['target']
        config = request.data['config']
        diff = NapalmHelper.configure_device(target=target, config=config)
        response = {'diff': diff}
        return Response(response)

        #return super(ConfigRequestList, self).create(request, *args, **kwargs)
