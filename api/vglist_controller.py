from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import Profile
from vglists.models import VideogameList

from .IGDBApi import update_game, update_list
from .serializers import (ProfileSerializer, ProfileVideogameListSerializer,
                          VideogameListSerializer, VideogameSerializer)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_vglist(request):

    try:
        title = request.data['title']
        description = request.data['description']
        list = request.data['list']
        id = request.data['id']

    except:
        return Response({
            "ok": False,
            "message": 'Missing fields'
        }, status=400)

    try:

        profile = Profile.objects.get(id=id)
    except:
        return Response({
            "ok": False,
            "message": 'User not found'
        }, status=400)

    if request.user != profile.user:
        return Response({
            "ok": False,
            "message": 'You are not authorized to create a list for this user'
        }, status=403)

    serializer = VideogameListSerializer(data={
        'title': title,
        'description': description,
        'list': list,
        'owner': profile.id
    })  # type: ignore

    if serializer.is_valid():
        vglist = serializer.save()
        update_list(list)

        for game in list:
            serializer = VideogameSerializer(data={
                'title': game['title'],
                'year': game['year'],
                'description': game['description'],
                'rating': game['rating'],
                'review': game['review'],
                'image_url': game['image_url'],
                'list': vglist.id
            })  # type: ignore

            if serializer.is_valid():
                serializer.save()
            

        #! change owner info of owner
        serializer = VideogameListSerializer(vglist)
        games_serializer = VideogameSerializer(
            vglist.videogames.all(), many=True)
        data = serializer.data
        data['games'] = games_serializer.data
        data['owner'] = ProfileSerializer(profile).data

        return Response({
            "ok": True,
            "list": data,
            "message": 'List created successfully'
        }, status=201)

    

    return Response('create_vglist')


@api_view(['GET'])
def get_vglist(request, pk):
    try:
        vglist = VideogameList.objects.get(id=pk)
    except:
        return Response({
            "ok": False,
            "message": 'List not found'
        }, status=404)

    serializer = VideogameListSerializer(vglist)

    data = serializer.data

    data['owner'] = ProfileSerializer(vglist.owner).data

    return Response({
        "ok": True,
        "list": data
    }, status=200)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_vglist(request, pk):
    try:
        vglist = VideogameList.objects.get(id=pk)
    except:
        return Response({
            "ok": False,
            "message": 'List not found'
        }, status=404)

    if not set(request.data.keys()) & {'title', 'description', 'is_sorted', 'list'}:
        return Response({
            "ok": False,
            "message": 'Missing fields'
        }, status=400)

    if request.user != vglist.owner.user:
        return Response({
            "ok": False,
            "message": 'You are not authorized to update this list'
        }, status=403)

    if 'list' in request.data:
        game_list_from_request = request.data['list']
        try:
            update_or_create_videogames(game_list_from_request, vglist)
        except Exception as e:
            return Response({
                "ok": False,
                "message": str(e)
            }, status=400)

    serializer = VideogameListSerializer(
        vglist, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        data = serializer.data
        data['owner'] = ProfileSerializer(vglist.owner).data

        return Response({
            "ok": True,
            "message": 'List updated successfully',
            "list": data
        }, status=200)

    else:
        return Response({
            "ok": False,
            "message": "Error updating list"
        }, status=400)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_vglist(request, pk):
    try:
        vglist = VideogameList.objects.get(id=pk)
    except:
        return Response({
            "ok": False,
            "message": 'List not found'
        }, status=404)

    if request.user != vglist.owner.user:
        return Response({
            "ok": False,
            "message": 'You are not authorized to delete this list'
        }, status=403)

    vglist.delete()

    return Response({
        "ok": True,
        "message": 'List deleted'
    }, status=200)


def update_or_create_videogames(game_list_from_request, vglist):

    request_game_ids = [game['id'] for game in game_list_from_request]

    # Iterate through all games in the `vglist`
    for videogame in vglist.videogames.all():
        # If the game is not in the request, delete it from the `vglist`
        if str(videogame.id) not in request_game_ids:
            videogame.delete()
        # Otherwise, update the game's fields from the request
        else:
            for game in game_list_from_request:
                if game['id'] == str(videogame.id):
                    for field in ['rating', 'review']:
                        if field in game:
                            setattr(videogame, field, game[field])
                    videogame.save()

                    game_list_from_request.remove(game)


    # Iterate through all games in the request
    for game in game_list_from_request:

        # If the game is not in the `vglist`, create a new game


        new_game = update_game(game['id'])


        serializer = VideogameSerializer(data={
            'title': game['title'],
            'year': new_game['year'],
            'description': new_game['description'],
            'rating': game['rating'],
            'review': game['review'],
            'image_url': game['image_url'],
            'list': vglist.id
        })  # type: ignore

        if serializer.is_valid():
            serializer.save()
        

#! denle this


@api_view(['GET'])
def get_all_user_vglists(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return Response({
            "ok": False,
            "message": 'Profile not found'
        }, status=404)

    # get only the first 5 lists

    vglists = profile.lists.all()  # type: ignore

    serializer = ProfileVideogameListSerializer(vglists, many=True)

    data = serializer.data

    return Response({
        "ok": True,
        "lists": data
    }, status=200)
