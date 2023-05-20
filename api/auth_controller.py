# Create your views here.
import os
import time

#! BOTO3
import boto3
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import Profile

from .JWT import (get_tokens_for_user, get_user_from_token,
                  refresh_token_for_user)
from .serializers import (ProfileVideogameListSerializer, UserSerializer,
                          ViewProfileSerializer)

#! move to helpers
#! send token as header x-token

#! API AUTH TOKEN


#! ENVIROMENT VARIABLES
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
REGION_NAME = os.environ["REGION_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

# !!!!!!!!!!!!!!!!!!!!!

#! crate serializer for this


def get_user_info(user):
    profile = user.profile
    return {
        'id': profile.id,
        'username': user.username,
        'name': profile.name,
        'email': user.email,
        'bio': profile.bio,
        'image_url': profile.image_url,
    }


#! WELCOME MAIL



@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        res = {
            'ok': True,
        }

        res.update(get_user_info(user))
        res.update(tokens)  # type: ignore

        return Response(res, status=201)
    else:
        error_dic = serializer.errors
        for field in error_dic:
            error_dic[field] = error_dic[field][0].title()


        message = list(error_dic.values())[0]

        res = {
            'ok': False,
            'message': message,
        }

        return Response(res, status=500)


@api_view(['POST'])
def login_user(request):
    password = request.data['password']
    email = request.data['email']

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        tokens = get_tokens_for_user(user)

        res = {
            'ok': True,
        }

        res.update(get_user_info(user))
        res.update(tokens)  # type: ignore

        return Response(res, status=200)
    else:
        res = {
            'ok': False,
            'message': 'Invalid credentials',
        }

        return Response(res, status=401)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request, pk):

    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

        profile = Profile.objects.get(pk=pk)

        user = profile.user

        if request.user != user:
            raise PermissionDenied(
                "You are not authorized to update this profile.")

        profile.name = request.data['name']
        profile.bio = request.data['bio']

        url = profile.image_url

        if url:
            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=f"profiles/{url.split('/')[-1]}"
            )

        if 'image' in request.FILES:


            image = request.FILES['image']

            key = f"profiles/{profile.id}-{int(time.time())}.png"

            s3.put_object(Bucket=BUCKET_NAME, Key=key,
                          Body=image, CacheControl='no-cache', ACL='public-read')

            profile.image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"

        profile.save()

        res = {
            'ok': True,
        }

        res.update(get_user_info(user))

        return Response(res, status=200)

    except Exception as e:

        res = {
            'ok': False,
            'message': 'Something went wrong',
        }

        return Response(res, status=500)


@api_view(['POST'])
def logout_user(request):
    logout(request)

    res = {
        'ok': True,
        'message': 'Logged out successfully',
    }

    return Response(res, status=200)


@api_view(['POST'])
def renew_token(request):
    refresh_token = request.data['refreshToken']

    try:

        tokens = refresh_token_for_user(refresh_token)

        if tokens is None:
            raise Exception('Invalid token')

        user = get_user_from_token(tokens['accessToken'])

        if user is None:
            raise Exception('Invalid token')


        res = {
            'ok': True,
        }

        res = get_user_info(user)
        res.update(tokens)


        return Response(res, status=200)

    except Exception as e:
        res = {
            'ok': False,
            'message': 'Invalid token',
        }

        return Response(res, status=500)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        user = profile.user
        if request.user != user:
            raise PermissionDenied(
                "You are not authorized to delete this user.")

        return Response({
            "ok": True,
            "message": 'User deleted'
        }, status=200)

    except Profile.DoesNotExist:
        return Response({
            "ok": False,
            "message": 'User not found'
        }, status=404)


@api_view(['GET'])
def get_profile_info(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return Response({
            "ok": False,
            "message": 'Profile not found'
        }, status=404)

    profile_serializer = ViewProfileSerializer(profile)

    vglists = profile.lists.all()  # type: ignore

    vglists_serializer = ProfileVideogameListSerializer(vglists, many=True)

    profile_data = profile_serializer.data

    vglists_data = vglists_serializer.data

    profile_data['lists'] = vglists_data

    return Response({
        "ok": True,
        "profile": profile_data
    }, status=200)
