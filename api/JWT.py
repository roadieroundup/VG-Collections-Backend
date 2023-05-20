from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import User


def get_tokens_for_user(user):
    token = TokenObtainPairSerializer.get_token(user)
    return {
        'refreshToken': str(token),
        'accessToken': str(token.access_token),
    }


def refresh_token_for_user(refreshToken):

    try:

        refresh = RefreshToken(refreshToken)

        return {
            'refreshToken': str(refresh),
            'accessToken': str(refresh.access_token),
        }
    except Exception as e:
        # Handle token refresh failure
        return None


def get_user_from_token(accessToken):

    try:
        # decode the access token
        token = AccessToken(accessToken)
        # get the user ID from the decoded token's payload
        user_id = token['user_id']
        # get the user object based on the user ID
        user = User.objects.get(id=user_id)
        return user
    except InvalidToken as e:
        # handle invalid token error
        return None
