from django.shortcuts import render
from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import Http404
import sys

from nodes.models import Group, Node
from .models import ConfigRequest, StatusMessage

from .tasks import configure_device_task

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
        req = ConfigRequest(target=target, config=config)
        req.save()
        diff = configure_device_task.delay(target=target, config=config, req=req.id)
        response = {'request-id': req.id}
        return Response(response)

        #return super(ConfigRequestList, self).create(request, *args, **kwargs)

class StatusRequestView(APIView):
    def get_object(self, pk):
        try:
            confreq = ConfigRequest.objects.get(pk=pk)
        except ConfigRequest.DoesNotExist:
            raise Http404

        if confreq.statusmessage_set.count() > 0:
            return confreq
        else:
            raise Http404

    def get(self, request, pk):
        confreq = self.get_object(pk=pk)
        msg = confreq.statusmessage_set.get()

        response = {'status': msg.status, 'result': msg.result}
        return Response(response)

    def post(self, request, pk):
        confreq = self.get_object(pk=pk)
        target = confreq.target
        config = confreq.config
        diff = configure_device_task.delay(target=target, config=config, req=confreq.id, commit=True)
        response = {'message': 'Committing configuration'}
        return Response(response)
