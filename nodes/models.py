from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    enable_password = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name

class Node(models.Model):
    hostname = models.CharField(max_length=255)
    ipv4 = models.CharField(max_length=255)
    ipv6 = models.CharField(max_length=255, blank=True)
    driver = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return self.hostname
