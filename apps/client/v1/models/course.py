from django.db import models

from .user import SimpleUser


class CourseType(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Course(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner_id = models.IntegerField()
    thumb_url = models.URLField()
    cover_url = models.URLField()
    description = models.TextField()
    last_activity = models.DateTimeField()
    total_score = models.IntegerField()
    total_tasks = models.IntegerField()
    unchangeable = models.BooleanField()
    include_weekly_report = models.BooleanField()
    content_type = models.IntegerField()
    is_netology = models.BooleanField()
    bg_url = models.URLField()
    video_url = models.URLField()
    demo = models.BooleanField()
    custom_author_names = models.CharField(max_length=64)
    custom_contents_link = models.URLField()
    hide_viewer_navigation = models.BooleanField()
    duration = models.IntegerField()
    authors = models.ManyToManyField(SimpleUser)
    types = models.ManyToManyField(CourseType)
