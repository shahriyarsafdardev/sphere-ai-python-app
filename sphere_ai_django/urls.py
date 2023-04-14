from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from user.views.user_api_view import UserGoogleLoginView, UserLoginView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', UserLoginView.as_view(),
         name='user_login'),
    path('api/v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/login/google/', UserGoogleLoginView.as_view(),
         name='user_google_login'),
    path('api/v1/logout/', UserLogoutView.as_view(),
         name='user_logout'),
    path('api/v1/', include('user.urls'))
]
