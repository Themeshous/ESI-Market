# Generated by Django 3.2.9 on 2022-10-03 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suivi', '0004_auto_20221003_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='op_dos',
            name='montant',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name="Montant de l'offre déposée"),
        ),
    ]
