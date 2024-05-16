"""Database Models."""
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)



class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a new user with given email and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email=email), **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
        
    def create_superuser(self, email, password):
        """
        Create a superuser and return.
        """
        user = self.create_user(email, password)
        user.is_staff = True 
        user.is_superuser = True
 
        user.save(using=self._db)
        
        return user
        
              
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    preferred_theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')


    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
    
    
class Task(models.Model):
    """Task model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
         editable=False)
    name = models.CharField(max_length=255, validators=[
        validators.MinLengthValidator(limit_value=3, message='Task name should be minimum 3 characters.')
    ])
    done = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
