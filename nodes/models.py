from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    enable_password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Node(models.Model):
    DRIVERS = (
        ('eos', 'Arista EOS'),
        ('junos', 'Juniper JUNOS'),
        ('iosxr', 'Cisco IOS-XR'),
        ('nxos', 'Cisco NXOS'),
        ('ios', 'Cisco IOS'),
        ('none', 'No driver')
    )

    hostname = models.CharField(max_length=255, unique=True)
    ipv4 = models.CharField(max_length=255, blank=True)
    ipv6 = models.CharField(max_length=255, blank=True)
    driver = models.CharField(max_length=255, choices=DRIVERS)
    comment = models.TextField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.hostname

class Interface(models.Model):
    SOURCES = (
        ('napalm', 'NAPALM'),
        ('manual', 'MANUAL')
    )

    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    enabled = models.BooleanField()
    speed = models.IntegerField(null=True)
    mac_address = models.CharField(max_length=255, null=True)
    source = models.CharField(max_length=255, choices=SOURCES)
    discovered = models.DateTimeField()
