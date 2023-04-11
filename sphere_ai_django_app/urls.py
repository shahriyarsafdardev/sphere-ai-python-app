from django.urls import path
from .views import *

urlpatterns = [
  path('postgres_references', postgres_references),
  path('postgres_reference/search', postgres_search),
  path('postgres_references/<str:id>', show_postgres_reference),
  path('hubspot_references', hubspot_references),
  path('hubspot_reference/search', hubspot_search),
  path('hubspot_references/<str:id>', show_hubspot_reference)
]