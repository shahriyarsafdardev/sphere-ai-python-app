from rest_framework import serializers
from user.models.hubspot_reference import HubspotReference


class HubspotReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubspotReference
        fields = (
            'id',
            'name',
            'environment',
            'hubspot_access_token',
        )
        extra_kwargs = {'hubspot_access_token': {'write_only': True}}
