# Generated by Django 4.1.6 on 2023-05-29 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0019_merge_20230529_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_mobile',
            name='modelo',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
