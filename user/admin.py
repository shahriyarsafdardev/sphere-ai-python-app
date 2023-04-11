from django.contrib import admin
from user.models.hubspot_reference import HubspotReference
from user.models.postgres_reference import PostgresReference

admin.site.register(PostgresReference)
admin.site.register(HubspotReference)
