# Generated by Django 5.0.2 on 2024-02-25 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0009_produitnc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='name',
            field=models.CharField(choices=[('Al', 'Alimentaire'), ('Mb', 'Meuble'), ('Sn', 'Sanitaire'), ('Vs', 'Vaisselle'), ('Vt', 'Vêtement'), ('Jx', 'Jouets'), ('Lg', 'Linge de Maison'), ('Bj', 'Bijoux'), ('Dc', 'Décor'), ('EL', 'Electromanager')], default='Alimentaire', max_length=50),
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCde', models.DateField(default=datetime.date.today, null=True)),
                ('totalCde', models.DecimalField(decimal_places=3, max_digits=10)),
                ('produits', models.ManyToManyField(to='magasin.produits')),
            ],
        ),
    ]