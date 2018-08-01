#!/usr/bin/env python
import os, sys
from napalm.base import get_network_driver
import socket
from datetime import datetime


if __name__ == '__main__':
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "viconf.settings")

    # Setup django
    import django
    django.setup()

    from nodes.models import Node, Interface

    nodes = Node.objects.all()

    for node in nodes:
        if node.driver != "none":
            driver = get_network_driver(node.driver)
            username = node.group.username
            password = node.group.password
            optional_args = {'enable_password': node.group.enable_password}
            try:
                target = socket.gethostbyname(node.hostname)
            except socket.error:
                if node.ipv4 is not None:
                    target = node.ipv4
                else:
                    pass

            with driver(target, username, password, optional_args=optional_args) as device:
                print("Connecting to device {}".format(target))
                interfaces = device.get_interfaces()

                for interface, options in interfaces.items():
                    if Interface.objects.filter(node=node).filter(name=interface).count() == 0:
                        print("Adding interface {}".format(interface))
                        iface = Interface()
                        iface.name = interface
                        iface.node = node
                        iface.description = options['description']
                        iface.enabled = options['is_enabled']
                        iface.mac_address = options['mac_address']
                        iface.speed = options['speed']
                        iface.source = "napalm"
                        iface.discovered = datetime.now()
                        iface.save()
