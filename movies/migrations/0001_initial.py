# Generated by Django 4.0.5 on 2022-06-24 13:08

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('image_link', models.CharField(max_length=50)),
                ('trailer_link', models.CharField(max_length=50)),
                ('imdb_rating', models.FloatField(max_length=3)),
                ('metacritic_rating', models.IntegerField()),
                ('tmd_rating', models.FloatField()),
                ('rotten_rating', models.IntegerField()),
                ('streaming_sources', jsonfield.fields.JSONField()),
            ],
        ),
    ]
