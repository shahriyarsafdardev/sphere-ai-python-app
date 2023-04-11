from django.urls import path
from .views.postgres_reference_api_view import postgres_search, postgres_references
from .views.hubspot_reference_api_view import hubspot_search, hubspot_references

urlpatterns = [
    path('postgres_references', postgres_references),
    path('postgres_references/<str:id>/query', postgres_search),
    path('hubspot_references/<str:id>/query', hubspot_search),
    path('hubspot_references', hubspot_references)
]
