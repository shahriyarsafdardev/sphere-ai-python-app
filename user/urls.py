from django.urls import path
from user.views.user_api_view import UserAccountView, UserCreateView
from .views.postgres_reference_api_view import PostgresReferencesView, PostgresSearchView
from .views.hubspot_reference_api_view import HubspotReferencesView, HubspotSearchView
from .views.document_api_view import BingSearchView
from .views.otp_secret_api_view import OTPSecretCreateView, OTPSecretVerifyView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user_create'),
    path('users/my_account/', UserAccountView.as_view(), name='user_account'),
    path('postgres_references/', PostgresReferencesView.as_view(),
         name='postgres_references/'),
    path('postgres_references/<str:id>/query/',
         PostgresSearchView.as_view(), name='postgres_search'),
    path('hubspot_references/',  HubspotReferencesView.as_view(),
         name='hubspot_references'),
    path('hubspot_references/<str:id>/query/',
         HubspotSearchView.as_view(), name='hubspot_search'),
    path('documents/search/', BingSearchView.as_view(), name='bing_search'),
    path('create_otp_secret/', OTPSecretCreateView.as_view(), name='create_otp'),
    path('verify_otp/', OTPSecretVerifyView.as_view(), name='verify_otp')
]
