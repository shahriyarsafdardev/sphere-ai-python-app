from django.urls import path
from .views import *

urlpatterns = [
  path('postgres_references', postgres_references),
  path('postgres_reference/search', postgres_search),
  path('postgres_reference/<reference_id>', show_postgres_reference),
  path('hubspot_references', hubspot_references),
  path('hubspot_reference/<reference_id>', show_hubspot_reference)
]