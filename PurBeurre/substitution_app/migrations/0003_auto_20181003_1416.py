# Generated by Django 2.0.7 on 2018-10-03 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitution_app', '0002_auto_20180924_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productsa',
            options={'managed': True, 'verbose_name': 'Produits A'},
        ),
        migrations.AlterModelOptions(
            name='userproducts',
            options={'managed': True, 'verbose_name': 'Produits utilisateur'},
        ),
    ]