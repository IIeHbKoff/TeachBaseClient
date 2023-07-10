from django.db import models

from .course import Course
from .label import Label


class CourseSession(models.Model):
    name = models.CharField(max_length=256)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    infinitely = models.BooleanField(default=False)
    access_type = models.CharField()
    finished = models.BooleanField(default=False)
    apply_url = models.URLField(blank=True, null=True)
    deadline_soon = models.BooleanField(default=False)
    assignments_count = models.IntegerField()
    deadline_type = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=256)
    period = models.IntegerField(blank=True, null=True)
    labels = models.ManyToManyField(Label)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

