"""
    Test for models.
"""
from django.test import TestCase
from todo.models import Task
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def create_user(email='test@example.com', password='testpassword'):
    """
    Function that creates a new user and return user.
    """
    return get_user_model().objects.create(email=email, password=password)


def create_task(name='task name', user=None):
    """
    Function create and return task.
    """
    return Task.objects.create(name=name, user=user)


class UserModelTests(TestCase):
    """Tests for User model."""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
            
    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')
            
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_user_theme_changed(self):
        """Test the theme change on user update."""
        user = create_user()
        user.preferred_theme = 'dark'
        user.save()
        
        self.assertEqual(user.preferred_theme, 'dark')
      
        
class TaskModelTests(TestCase):
    """Test for Task Model."""
    def test_task_create_success(self):
        """Test create task success."""
        user = create_user()
        new_task = create_task(user=user)
        
        task = Task.objects.get(id=new_task.id)
        
        self.assertEqual(task.name, new_task.name)
        self.assertEqual(task.user.name, new_task.user.name)
        
    def test_task_name_blank_raises_error(self):
        """Task name being blank raises error."""
        user = create_user()
        task_instance = Task(user=user)
        
        with self.assertRaises(ValidationError) as context:
            task_instance.full_clean()
            
        # print(context.exception.message_dict)
        self.assertEqual(context.exception.message_dict['name'][0],
                         'This field cannot be blank.')
    
    def test_task_name_low_characters_raises_error(self):
        """Test the task name with less characters raises validation error."""
        
        user =create_user()
        task_instance = Task(name='ab', user=user)
        
        with self.assertRaises(ValidationError) as context:
            task_instance.full_clean()
            
        self.assertEqual(context.exception.message_dict['name'][0],
                         'Task name should be minimum 3 characters.')
    
    def test_task_with_no_user_raises_error(self):
        """Test the task creation fails with no user assigned."""
        task_instance = Task(name='Go to the gym')
        
        with self.assertRaises(ValidationError) as context:
            task_instance.full_clean()
            
        self.assertEqual(context.exception.message_dict['user'][0],
                         'This field cannot be null.')
        
        
    