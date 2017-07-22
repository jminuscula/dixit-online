
# from django.db import IntegrityError
# from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import NotFound
# from rest_framework.response import Response
from rest_framework import generics  # , status

from dixit.api.auth.serializers.user import UserSerializer


class Me(generics.RetrieveAPIView):
    """
    Retrieves currently logged user info
    """

    model = User
    serializer_class = UserSerializer

    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
