from django.db import models


class SimpleUser(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    external_id = models.CharField(max_length=32)
    role_id = models.IntegerField()
    auth_type = models.IntegerField()
    last_activity_at = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    lang = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.id} {self.name} {self.last_name}"
