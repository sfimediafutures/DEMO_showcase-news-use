# Generated by Django 4.1 on 2022-10-20 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0002_alter_entry_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='session',
        ),
    ]