# Generated by Django 2.0.7 on 2018-07-05 13:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodes', '0003_auto_20180704_0551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_config', models.TextField()),
                ('down_config', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('defaults', django.contrib.postgres.fields.jsonb.JSONField()),
                ('description', models.CharField(max_length=255)),
                ('require_update', models.BooleanField()),
                ('deleted', models.BooleanField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255)),
                ('customer', models.CharField(max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('speed', models.IntegerField(null=True)),
                ('product', models.CharField(max_length=255, null=True)),
                ('template_fields', django.contrib.postgres.fields.jsonb.JSONField()),
                ('deleted', models.BooleanField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.Form')),
                ('node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodes.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255, null=True)),
                ('up_contents', models.TextField()),
                ('down_contents', models.TextField()),
                ('fields', django.contrib.postgres.fields.jsonb.JSONField()),
                ('deleted', models.BooleanField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='templates',
            field=models.ManyToManyField(to='configuration.Template'),
        ),
        migrations.AddField(
            model_name='config',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='configuration.Service'),
        ),
    ]