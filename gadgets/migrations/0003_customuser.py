# Generated by Django 4.0.2 on 2022-03-15 21:38

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('gadgets', '0002_rename_aquisition_type_gadget_acquisition_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
