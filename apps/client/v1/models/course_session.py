from django.db import models

from .course import Course
from .label import Label


class CourseSession(models.Model):
    name = models.CharField(max_length=256)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    course_id = models.IntegerField()
    infinitely = models.BooleanField()
    access_type = models.CharField()
    finished = models.BooleanField()
    apply_url = models.URLField()
    deadline_soon = models.BooleanField()
    assignments_count = models.IntegerField()
    deadline_type = models.IntegerField()
    slug = models.CharField(max_length=256)
    period = models.IntegerField()
    labels = models.ManyToManyField(Label)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

