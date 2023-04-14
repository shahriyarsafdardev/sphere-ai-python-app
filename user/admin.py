from django.contrib import admin
from user.models.company import Company
from user.models.document import Document
from user.models.hubspot_reference import HubspotReference
from user.models.postgres_reference import PostgresReference
from user.models.user import User

admin.site.register(PostgresReference)
admin.site.register(HubspotReference)
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Document)
