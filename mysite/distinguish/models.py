from django.db import models


class Photo(models.Model):
    photoName = models.CharField(max_length=50)
    distinguishType = models.IntegerField(default=1)
    path = models.CharField(max_length=100)
    postDate = models.DateTimeField('date published')

