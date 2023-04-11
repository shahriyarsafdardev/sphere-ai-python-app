from django.urls import path
from .views import *

urlpatterns = [
  path('postgres_references', postgres_references),
  path('postgres_references/<str:id>', show_postgres_reference),
  path('postgres_references/<str:id>/query', postgres_search),
  path('hubspot_references', hubspot_references),
  path('hubspot_references/<str:id>', show_hubspot_reference),
  path('hubspot_references/<str:id>/query', hubspot_search)
]