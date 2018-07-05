# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from viconf.celery import app
from .models import ConfigRequest, StatusMessage

from util.napalmhelper import NapalmHelper

@app.task
def configure_device_task(target, config, req, commit=False):
    confreq = ConfigRequest.objects.get(pk=req)
    if confreq.statusmessage_set.count() > 0:
        msg = confreq.statusmessage_set.get()
    else:
        msg = StatusMessage(request=confreq, status="Pending")
        msg.save()

    config = config.encode().decode('unicode_escape')
    diff = NapalmHelper.configure_device(target, config, commit)
    if commit:
        msg.status = "DONE"
    else:
        msg.status = "READY"
    msg.result = diff
    msg.save()
