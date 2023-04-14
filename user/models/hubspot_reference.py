import uuid
from django.db import models


class HubspotReference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, null=False, default="")
    hubspot_access_token = models.CharField(
        max_length=255, null=False, default="")
    environment = models.CharField(max_length=255, null=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
