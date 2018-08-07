from django.db import models
from django.contrib.postgres.fields import JSONField
from nodes.models import Node
from django.forms import ModelForm


# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    platform = models.CharField(max_length=255,  null=True)
    up_contents = models.TextField()
    down_contents = models.TextField()
    fields = JSONField(null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Form(models.Model):
    name = models.CharField(max_length=255)
    defaults = JSONField()
    description = models.CharField(max_length=255)
    require_update = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    templates = models.ManyToManyField(Template)


class Service(models.Model):
    reference = models.CharField(max_length=255)
    customer = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    speed = models.IntegerField(null=True)
    product = models.CharField(max_length=255, null=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    template_fields = JSONField()
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)


class Config(models.Model):
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    up_config = models.TextField()
    down_config = models.TextField()
    created = models.DateTimeField(auto_now=True)


class Link(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    node = models.ManyToManyField(Node)


class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = [
            "name",
            "description",
            "platform",
            "up_contents",
            "down_contents"
        ]


class FormForm(ModelForm):
    class Meta:
        model = Form
        fields = [
            "name",
            "description",
            "defaults",
            "templates"
        ]
