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
    thumb_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    total_score = models.IntegerField()
    total_tasks = models.IntegerField()
    unchangeable = models.BooleanField(default=False)
    include_weekly_report = models.BooleanField()
    content_type = models.IntegerField(blank=True, null=True)
    is_netology = models.BooleanField(default=False)
    bg_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    demo = models.BooleanField(default=False)
    custom_author_names = models.CharField(max_length=64, blank=True, null=True)
    custom_contents_link = models.URLField(blank=True, null=True)
    hide_viewer_navigation = models.BooleanField(default=False)
    duration = models.IntegerField(blank=True, null=True)
    authors = models.ManyToManyField(SimpleUser)
    types = models.ManyToManyField(CourseType)
