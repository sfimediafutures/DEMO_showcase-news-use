# Generated by Django 4.1 on 2022-11-02 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0007_alter_entry_entry_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='total_time',
            field=models.IntegerField(default=0),
        ),
    ]