from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from user.views.user_api_view import UserLoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', UserLoginView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('user.urls'))
]
