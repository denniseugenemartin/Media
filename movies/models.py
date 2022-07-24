from django.db import models
from jsonfield import JSONField

class Media(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    imdb_rating = models.FloatField(max_length=4, null=True, blank=True)
    stream_sources = models.JSONField(null=True, blank=True)
    rank = models.IntegerField(null = True, blank = True)
    type = models.CharField(max_length=50, null=True, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    metacritic_score = models.FloatField(null=True, blank=True)
    date_updated = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.id

