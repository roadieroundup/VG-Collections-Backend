# Generated by Django 4.1.7 on 2023-04-24 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vglists', '0002_remove_videogamelist_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogame',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='review',
            field=models.TextField(blank=True),
        ),
    ]