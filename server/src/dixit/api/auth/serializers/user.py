
from rest_framework import serializers
from django.contrib.auth.models import User

from dixit.account.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name', )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User objects
    """
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile', )
