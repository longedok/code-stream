from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    description = models.TextField()
    status = (('o', 'Official'),
              ('p', 'Private'))


class Topic(models.Model):
    name = models.CharField(max_length=100)


class Stream(models.Model):
    name = models.CharField(max_length=100)