# Generated by Django 4.1.6 on 2023-08-09 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0003_inventoryactivities'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryactivities',
            old_name='action',
            new_name='motivo',
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='colaborador',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='colaborador_novo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='inventario',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='local',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='local_novo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inventoryactivities',
            name='patrimonio',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
