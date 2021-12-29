from django.urls import re_path, path

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token  # accounts app

from .views import AuthAPIView, RegisterAPIView

urlpatterns = [
    re_path(r'^$', AuthAPIView.as_view(), name='login'),
    re_path(r'^register/$', RegisterAPIView.as_view(), name='register'),
    re_path(r'^jwt/$', obtain_jwt_token),
    re_path(r'^jwt/refresh/$', refresh_jwt_token),
]
