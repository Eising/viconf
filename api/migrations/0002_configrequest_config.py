# Generated by Django 2.0.7 on 2018-07-04 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configrequest',
            name='config',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]