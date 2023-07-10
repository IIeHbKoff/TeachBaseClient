from django.db import models


class SimpleUser(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    external_id = models.CharField(max_length=32, blank=True, null=True)
    role_id = models.IntegerField()
    auth_type = models.IntegerField()
    last_activity_at = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    locked = models.BooleanField(default=True)
    lang = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.id} {self.name} {self.last_name}"
