# Generated by Django 4.1.6 on 2023-06-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0022_alter_colaborador_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='colaborador',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='inventory_mobile',
            name='modelo',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
