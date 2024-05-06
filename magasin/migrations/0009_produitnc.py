# Generated by Django 5.0.2 on 2024-02-25 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0008_fournisseur_produits_fournisseur'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProduitNC',
            fields=[
                ('produits_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='magasin.produits')),
                ('duree_garantie', models.CharField(max_length=100)),
            ],
            bases=('magasin.produits',),
        ),
    ]