# Generated by Django 5.0.1 on 2024-08-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0002_alter_commande_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='ref',
            field=models.CharField(default=3604617, max_length=255),
        ),
        migrations.AlterField(
            model_name='commande',
            name='tel',
            field=models.CharField(max_length=10),
        ),
    ]
