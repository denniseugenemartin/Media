from django.db import models
from jsonfield import JSONField

class Movie(models.Model):
    id = models.CharField(max_length=50, primary_key=True)


    def __str__(self):
        return self.id

