# Generated by Django 4.0.5 on 2022-07-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
