from django.db import models
from django.contrib.auth.models import User

import model_utils.fields as util_fields
import model_utils.models as util_models


class Series(util_models.TimeStampedModel):
    title = models.CharField(max_length=100)

    owner = models.ForeignKey(User, related_name='series')


class Stream(models.Model):
    title = models.CharField(max_length=100)
    created = util_fields.AutoCreatedField()
    finished = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(User, related_name='streams')
    series = models.ForeignKey(Series, null=True, blank=True)


class ActiveStream(models.Model):
    stream = models.ForeignKey(Stream)
    viewers = models.IntegerField()
    preview_url = models.URLField()


class Techonology(util_models.TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()

    creator = models.ForeignKey(User)
    streams = models.ManyToManyField(Stream, related_name='technologies')
