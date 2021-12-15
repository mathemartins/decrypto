from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import re_path, path

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token  # accounts app

from .views import AuthAPIView, RegisterAPIView
from ..views import AccountEmailActivateView, UserProfileView

urlpatterns = [
    re_path(r'^$', AuthAPIView.as_view(), name='login'),
    re_path(r'^register/$', RegisterAPIView.as_view(), name='register'),
    re_path(r'^jwt/$', obtain_jwt_token),
    re_path(r'^jwt/refresh/$', refresh_jwt_token),

    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    re_path(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend-activation'),

    path('sign-out/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile'),
]
