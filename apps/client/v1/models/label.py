from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=256)
    group_id = models.IntegerField()
