from rest_framework import serializers
from user.models.postgres_reference import PostgresReference

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
