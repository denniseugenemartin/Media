from django.db import models
from jsonfield import JSONField

class Movie(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    image_link = models.CharField(max_length=50)
    trailer_link = models.CharField(max_length=50)
    imdb_rating = models.FloatField(max_length=3)
    metacritic_rating = models.IntegerField()
    tmd_rating = models.FloatField()
    rotten_rating = models.IntegerField()
    streaming_sources = JSONField()

    def __str__(self):
        return f'{{self.title}} ({{self.year}})'

