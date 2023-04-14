import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class PostgresReference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120, null=False)
    db_name = models.CharField(max_length=255, null=False)
    db_user_name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    host = models.CharField(max_length=255, null=False)
    port = models.IntegerField(null=False)
    documentation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
