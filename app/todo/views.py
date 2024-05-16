"""Views for api end points"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from todo import serializers


class UserRegisterAPIView(generics.CreateAPIView):
    """API View Class to create a new user."""
    serializer_class = serializers.UserSerializer
    

class CreateTokenView(ObtainAuthToken):
    """Create a new token for the authenticated user."""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
