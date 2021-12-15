import datetime
from django.utils import timezone

from rest_framework_jwt.settings import api_settings

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


def jwt_response_payload_handler(token, user=None, message=None, status: bool = None, status_code=None,  request=None):
    return {
        'message': message,
        'success': status,
        'status': status_code,
        'token': token,
        'user': user.username,
        'email': user.email,
        'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    }
