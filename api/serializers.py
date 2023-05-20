from rest_framework import serializers
from users.models import Profile
from vglists.models import VideogameList, Videogame
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        # this is the fields that will be received from the frontend
        fields = ['email', 'username', 'password']

    def validate_email(self, value):
        # Check if email is already in use
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email address is already in use")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError(
                "Username is already in use")

        # convert username to lowercase

        return value.lower()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # this is the fields that will be received from the frontend
        fields = '__all__'

class ViewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # this is the fields that will be received from the frontend
        fields = ('id', 'username', 'name', 'bio', 'image_url')
    

class VideogameListSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    games = serializers.SerializerMethodField()

    class Meta:
        model = VideogameList
        fields = ['id', 'created', 'title',
                  'description', 'is_sorted', 'owner', 'games']
        read_only_fields = ['id', 'created']

    # class Meta:
    #     model = VideogameList
    #     # this is the fields that will be received from the frontend
    #     fields = '__all__'

    def get_games(self, obj):
        games = VideogameSerializer(obj.videogames.all(), many=True).data

        for game in games:
            game.pop('list')

        return games

class ProfileVideogameListSerializer(serializers.ModelSerializer):
    games = serializers.SerializerMethodField()
    games_count = serializers.SerializerMethodField()


    class Meta:
        model = VideogameList
        fields = ('id', 'title', 'description', 'is_sorted', 'owner', 'games', 'games_count')

    def get_games(self, obj):
        games = obj.videogames.all()[:5] # limit to first 5 games
        serializer = VideogameSerializer(games, many=True)
        return serializer.data

    def get_games_count(self, obj):
        return obj.videogames.count()

class VideogameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videogame
        # this is the fields that will be received from the frontend
        fields = '__all__'
