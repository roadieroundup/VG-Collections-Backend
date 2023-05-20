from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)

    # Customize the response for JWT authentication errors
    if isinstance(exc, (AuthenticationFailed, InvalidToken, TokenError, NotAuthenticated)):

        response.data = {  # type: ignore
            'ok': False,
            'message': 'Authentication failed',
        }

        response.status_code = 401  # type: ignore

    return response
