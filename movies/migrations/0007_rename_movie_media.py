# Generated by Django 4.0.5 on 2022-07-17 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_movie_rotten_critic_score_movie_rotten_user_rating_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Movie',
            new_name='Media',
        ),
    ]
