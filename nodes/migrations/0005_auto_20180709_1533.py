# Generated by Django 2.0.7 on 2018-07-09 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0004_auto_20180709_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='ipv4',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
