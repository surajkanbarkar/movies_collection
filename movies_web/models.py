import uuid as uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserCollections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    genres = models.CharField(max_length=250, blank=True, null=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movies = models.JSONField()
    favourite_genres = models.BooleanField(default=0)

    def __str__(self):
        return str(self.uuid) + '----' + str(self.title)


class VisitorsCount(models.Model):
    count = models.IntegerField()

    def __str__(self):
        return self.count
