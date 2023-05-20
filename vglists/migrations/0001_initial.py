# Generated by Django 4.1.7 on 2023-03-13 10:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideogameList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
                ('is_sorted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Videogame',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('description', models.TextField()),
                ('rating', models.IntegerField()),
                ('review', models.TextField()),
                ('image_url', models.URLField()),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videogames', to='vglists.videogamelist')),
            ],
        ),
    ]
