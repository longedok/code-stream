from django.db import models
from django.contrib.auth.models import User

import model_utils.fields as util_fields
import model_utils.models as util_models


class Series(util_models.TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

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


class Technology(util_models.TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()

    creator = models.ForeignKey(User)
    streams = models.ManyToManyField(Stream, related_name='technologies')


class Material(util_models.TimeStampedModel):
    title = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()

    creator = models.ForeignKey(User)
    technology = models.ForeignKey(Technology, related_name='materials')


class Event(util_models.TimeStampedModel):
    STREAM_STARTED = 'stream_started'
    STREAM_FINISHED = 'stream_finished'
    TECHNOLOGY_ADDED = 'technology_added'
    MATERIAL_ADDED = 'material_added'
    EVENT_TYPE_CHOICES = (
        (STREAM_STARTED, 'Stream Started'),
        (STREAM_FINISHED, 'Stream Finished'),
        (TECHNOLOGY_ADDED, 'Technology Added'),
        (MATERIAL_ADDED, 'Material Added'),
    )

    user = models.ForeignKey(User, related_name='events')
    type = models.CharField(choices=EVENT_TYPE_CHOICES, max_length=30)
    description = models.TextField()