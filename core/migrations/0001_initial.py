# Generated by Django 2.1.1 on 2018-09-09 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_id', models.CharField(max_length=22)),
                ('spotify_user_id', models.TextField()),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Gosto!'), (2, 'Não gosto!')])),
                ('date_add', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Playlist',
                'verbose_name_plural': 'Playlists',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_id', models.CharField(max_length=22)),
                ('name', models.TextField()),
                ('duration_ms', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Música',
                'verbose_name_plural': 'Músicas',
            },
        ),
        migrations.CreateModel(
            name='TrackFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acousticness', models.DecimalField(decimal_places=14, max_digits=15)),
                ('danceability', models.DecimalField(decimal_places=14, max_digits=15)),
                ('energy', models.DecimalField(decimal_places=14, max_digits=15)),
                ('instrumentalness', models.DecimalField(decimal_places=14, max_digits=15)),
                ('key', models.PositiveSmallIntegerField()),
                ('liveness', models.DecimalField(decimal_places=14, max_digits=15)),
                ('loudness', models.DecimalField(decimal_places=12, max_digits=15)),
                ('mode', models.SmallIntegerField()),
                ('speechiness', models.DecimalField(decimal_places=14, max_digits=15)),
                ('tempo', models.DecimalField(decimal_places=12, max_digits=15)),
                ('time_signature', models.PositiveSmallIntegerField()),
                ('valence', models.DecimalField(decimal_places=14, max_digits=15)),
            ],
            options={
                'verbose_name': 'Característica da Música',
                'verbose_name_plural': 'Características das Músicas',
            },
        ),
        migrations.AddField(
            model_name='track',
            name='features',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.TrackFeatures'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(related_name='playlists', to='core.Track'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]