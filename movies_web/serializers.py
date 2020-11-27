from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserCollections


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', )


class UserCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollections
        fields = ('title', 'description', 'genres', 'movies', 'uuid', )

