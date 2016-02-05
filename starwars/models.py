from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from tracking_fields.decorators import track
from tracking_fields.models import TrackingEvent


@track('name', 'description')
class Movie(models.Model):
    """
        Movie
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    histo = GenericRelation(TrackingEvent, content_type_field='object_content_type')

    def episodes(self):
        return Episode.objects.filter(movie=self)

    def __str__(self):
        return "%s" % self.name

@track('name', 'scenario')
class Episode(models.Model):
    """
       Episode - for Trilogy and So on ;)
    """
    name = models.CharField(max_length=200)
    scenario = models.TextField()
    movie = models.ForeignKey(Movie)
    histo = GenericRelation(TrackingEvent, content_type_field='object_content_type')

    def __str__(self):
        return "%s" % self.name
