from django.urls import path
from user.views.user_api_view import UserAccountView, UserCreateView
from .views.postgres_reference_api_view import PostgresReferencesView, PostgresSearchView
from .views.hubspot_reference_api_view import hubspot_search, hubspot_references

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user_create'),
    path('users/my_account/', UserAccountView.as_view(), name='user_account'),
    path('postgres_references/', PostgresReferencesView.as_view(),
         name='postgres_references/'),
    path('postgres_references/<str:id>/query/',
         PostgresSearchView.as_view(), name='postgres_search'),
    path('hubspot_references/<str:id>/query/', hubspot_search),
    path('hubspot_references/', hubspot_references)
]
