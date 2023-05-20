from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .IGDBApi import recent_games, search_games


@api_view(['GET'])
def games_home(request):
    games = recent_games()

    return Response(games, status=200)


@api_view(['POST'])
def search_results(request):

    game_title = request.data['game_title']

    games = search_games(game_title)

    if not games:
        return Response({'ok': False, 'message': 'No games found'}, status=404)

    return Response(games, status=200)
