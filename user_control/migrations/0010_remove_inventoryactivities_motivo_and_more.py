# Generated by Django 4.1.6 on 2023-08-14 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0009_remove_inventoryactivities_created_at_formatted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryactivities',
            name='motivo',
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='motivo_depreciado',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
