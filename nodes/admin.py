from django.contrib import admin

# Register your models here.

from .models import Group, Node

admin.site.register(Group)
admin.site.register(Node)
