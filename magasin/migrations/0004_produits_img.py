from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produits',
            name='img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
