# Generated by Django 4.1.6 on 2023-08-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0004_rename_action_inventoryactivities_motivo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryactivities',
            name='created_at_formatted',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
