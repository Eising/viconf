# Generated by Django 2.0.7 on 2018-07-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_configrequest_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusmessage',
            name='result',
            field=models.TextField(blank=True),
        ),
    ]