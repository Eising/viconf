# Generated by Django 2.0.7 on 2018-07-31 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0008_auto_20180729_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
