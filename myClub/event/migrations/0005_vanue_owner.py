# Generated by Django 5.0.2 on 2025-02-20 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_manager_alter_event_vanue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vanue',
            name='owner',
            field=models.IntegerField(default=1, verbose_name='Vanue Owner'),
        ),
    ]
