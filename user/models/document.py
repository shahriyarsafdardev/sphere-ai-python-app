import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models.company import Company


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published_at = models.DateTimeField()
    title = models.CharField(max_length=120, default="", null=True)
    transcript = models.JSONField(default=list)
    url = models.CharField(max_length=255, null=False, default="")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
