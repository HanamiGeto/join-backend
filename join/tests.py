from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import date
from join.models import Category, Contact, Task

class UserViewSetTest(APITestCase):
    def test_list_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

class GroupViewSetTest(APITestCase):
    def test_list_groups(self):
        response = self.client.get('/groups/')
        self.assertEqual(response.status_code, 200)

class RegistrationViewTest(APITestCase):
    def test_registration(self):
        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post('/register/', data, format='json')
        self.assertEqual(response.status_code, 201)

class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test_password')

    def test_login_with_email_authentication(self):
        data = {'email': 'test@example.com', 'password': 'test_password'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)

class TaskListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test_password')
        self.token = Token.objects.create(user=self.user)

    def test_list_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': date.today(),
            'urgency': 'low', 
            'process_status': 'to-do',
            'category': {'title': 'TestCategory', 'color': 'blue'},
            'assigned_to': [{'name': 'TestUser1', 'email': 'test@test.de', 'phone': '651065165156', "initials": "SK", "initials_color": "rgb(221,70,60)"}],
            'subtasks': [{'title': 'Subtask 1', 'done': False}, {'title': 'Subtask 2', 'done': True}] 
        }
        response = self.client.post('/tasks/', data, format='json')
        self.assertEqual(response.status_code, 201)

class TaskDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test_password')
        self.token = Token.objects.create(user=self.user)
        self.task = Task.objects.create(title='Test Task', author=self.user, due_date=date.today(), category=Category.objects.create(title='TestCategory'))

    def test_retrieve_task(self):
        response = self.client.get(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_partial_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {'description': 'Updated Description'}
        response = self.client.patch(f'/tasks/{self.task.pk}/', data, format='json')
        self.assertEqual(response.status_code, 200)

class CategoryListViewTest(APITestCase):
    def test_list_categories(self):
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)

    def test_create_category(self):
        data = {'title': 'Test Category', 'color': 'blue'}
        response = self.client.post('/category/', data, format='json')
        self.assertEqual(response.status_code, 201)

class CategoryDetailViewTest(APITestCase):
    def test_retrieve_category(self):
        response = self.client.get('/category/1/')
        self.assertEqual(response.status_code, 200)

class SubtaskListViewTest(APITestCase):
    def test_list_subtasks(self):
        response = self.client.get('/subtask/')
        self.assertEqual(response.status_code, 200)

    def test_create_subtask(self):
        data = {'title': 'Test Subtask', 'done': False}
        response = self.client.post('/subtask/', data, format='json')
        self.assertEqual(response.status_code, 201)

class SubtaskDetailViewTest(APITestCase):
    def test_retrieve_subtask(self):
        response = self.client.get('/subtask/1/')
        self.assertEqual(response.status_code, 200)

class ContactListViewTest(APITestCase):
    def test_list_contacts(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_create_contact(self):
        data = {'name': 'Test Contact', 'email': 'test@example.com', 'phone': '651065165156', 'initials': 'TS', 'initials_color': 'rgb(221,70,60)'}
        response = self.client.post('/contact/', data, format='json')
        self.assertEqual(response.status_code, 201)

class ContactDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test_password')
        self.token = Token.objects.create(user=self.user)
        self.contact = Contact.objects.create(name='Test User', email='test@example.com', phone=651065165156, initials='TU', initials_color='rgb(221,70,60)')
        
    def test_retrieve_contact(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get('/contact/1/')
        self.assertEqual(response.status_code, 200)

    def test_partial_update_contact(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        data = {'email': 'updated@example.com'}
        response = self.client.patch(f'/contact/{self.contact.pk}/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_contact(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(f'/contact/{self.contact.pk}/')
        self.assertEqual(response.status_code, 204)