# Generated by Django 2.0.7 on 2018-07-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0005_auto_20180709_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='driver',
            field=models.CharField(choices=[('eos', 'Arista EOS'), ('junos', 'Juniper JUNOS'), ('iosxr', 'Cisco IOS-XR'), ('nxos', 'Cisco NXOS'), ('ios', 'Cisco IOS'), ('none', 'No driver')], max_length=255),
        ),
    ]