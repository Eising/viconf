# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from viconf.celery import app
from .models import ConfigTask
import socket
from napalm.base import get_network_driver


@shared_task
def push_to_device_task(pk, commit=False):
    configtask = ConfigTask.objects.get(pk=pk)
    config = configtask.config.encode().decode('unicode_escape')
    configtask.state = 'COMMUNICATING'
    configtask.save()
    node = config.service.node

    # This is important. We try to connect by the hostname primarily, but if
    # that fails, we try the IPv4 address instead. No connections over IPv6 are
    # made.
    try:
        target = socket.gethostbyname(node.hostname)
    except socket.error:
        target = node.ipv4

    vendor = node.driver
    username = node.group.username
    password = node.group.password
    optional_args = {'enable_password': node.group.enable_password}

    driver = get_network_driver(vendor)

    with driver(target, username, password, optional_args=optional_args) as device:
        device.load_merge_candidate(config=config)

        diff = device.compare_config()
        configtask.diff = diff
        configtask.state = 'READY'
        configtask.save()

        if commit:
            device.commit_config()
            configtask.state = 'DONE'
            configtask.save()

    return true
