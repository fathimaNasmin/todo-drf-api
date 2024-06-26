"""Test the api endpoints."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from todo.models import Task

from rest_framework.test import APIClient
from rest_framework import status


REGISTER_USER_URL = reverse('todo:register')
LOGIN_USER_URL = reverse('todo:login')
USER_PROFILE_URL = reverse('todo:profile')

TASK_URL = reverse('todo:task-list')


def task_detail_url(task_id):
    """return url for task detail."""
    return reverse('todo:task-detail', args=[task_id])


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
        
    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(USER_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(USER_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(USER_PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(USER_PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

class TaskAPITest(TestCase):
    """Test cases for task endpoints."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(self.user)
        self.task = Task.objects.create(user=self.user, name='Test Task')

    def test_get_tasks(self):
        """Test tasks retreival of authenticated user."""
        response = self.client.get(TASK_URL)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        """Test task creation successful."""
        data = {
            'name': 'New Task'
        }
        
        response = self.client.post(TASK_URL, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.data['name'], data['name'])

    def test_update_task(self):
        """Test task on updation success."""
        payload = {
            'name': 'Updated Task',
            'done': True
        }
        url = task_detail_url(self.task.id)
        response = self.client.patch(url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, payload['name'])
        self.assertTrue(self.task.done)

    def test_delete_task(self):
        """Test task delete endpoint."""
        url = task_detail_url(self.task.id)
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_unauthenticated_access(self):
        """Test access to unauthenticated user."""
        self.client.logout()
        
        response = self.client.get(TASK_URL)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(TASK_URL, {'name': 'Task'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.client.logout()