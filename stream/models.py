from django.db import models
from django.contrib.auth.models import User

import model_utils.fields as util_fields


class Stream(models.Model):
    title = models.CharField(max_length=100)
    created = util_fields.AutoCreatedField()
    finished = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(User, null=True, blank=True)


class ActiveStream(models.Model):
    stream = models.ForeignKey(Stream)
    viewers = models.IntegerField()
    preview_url = models.URLField()