# Generated by Django 5.0.1 on 2024-08-06 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0004_remove_commande_poids_alter_commande_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='prodName',
            field=models.CharField(max_length=200000000),
        ),
        migrations.AlterField(
            model_name='commande',
            name='ref',
            field=models.CharField(default=7176609, max_length=255),
        ),
    ]
