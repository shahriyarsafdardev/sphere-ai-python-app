from rest_framework import serializers
from .models import *

class PostgresReferenceSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostgresReference
    fields = [
      'id',
      'title',
      'db_name',
      'db_user_name',
      'host',
      'port'
    ]

class HubspotReferenceSerializer(serializers.ModelSerializer):
  class Meta:
    model = HubspotReference
    fields = [
      'id',
      'name',
      # 'hubspot_access_token',
      'environment'
    ]