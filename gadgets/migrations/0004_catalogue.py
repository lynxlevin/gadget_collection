# Generated by Django 4.0.2 on 2022-03-12 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gadgets', '0003_gift'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('gadget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gadgets.gadget')),
            ],
        ),
    ]