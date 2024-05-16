"""Test the api endpoints."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


REGISTER_USER_URL = reverse('todo:register')
LOGIN_USER_URL = reverse('todo:login')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test cases for public user api endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_create_user_successful(self):
        """Create user successfull."""
        payload = {
            'name': 'username',
            'email': 'user@example.com',
            'password': 'userpassword123245'
        }
        
        res = self.client.post(REGISTER_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short_error(self):
        """Test an error is returned if password less than 8 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
        
    def test_create_user_token(self):
        """Test creating a token for user by authenticating."""
        user_details = {
            'name': 'test name',
            'email': 'test@example.com',
            'password': 'tsetpass443'
        }
        create_user(**user_details)
        
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        
        res = self.client.post(LOGIN_USER_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_token_bad_credentials(self):
        """Test creation fails with bad credentials."""
        create_user(email='test@example.com', password='goodpass')
        
        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }
        
        res = self.client.post(LOGIN_USER_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(LOGIN_USER_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
