"""
Serializers for the todo app.
"""
from django.contrib.auth import (get_user_model, 
                                 authenticate)
from django.utils.translation import gettext as _

from rest_framework import serializers

from todo.models import Task


class UserSerializer(serializers.ModelSerializer):
    """Serialize the user object."""
    
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'preferred_theme']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }
        
    def create(self, validated_data):
        """Create a user with encrypted data."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return the user."""
        password = self.validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            instance.set_password(password)
            instance.save()
            
        return user
  
  
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token foe logging in."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        """Validate and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
    

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'