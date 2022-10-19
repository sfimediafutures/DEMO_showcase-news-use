# Generated by Django 4.1 on 2022-10-19 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0003_alter_entry_entry_id_alter_session_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='handler.session'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='source',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
