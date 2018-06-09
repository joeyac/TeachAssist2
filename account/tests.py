import json

from django.test import TestCase

from django.test import Client

from rest_framework import status

from account.models import User

from utils.constants import UserType


class AccountTestCase(TestCase):
    def setUp(self):
        teacher = User.objects.create(username='g123', email='g124@test.com', user_type=UserType.TEACHER)
        teacher.set_password('g123')
        teacher.save()
        self.c = Client()

    def send_json(self, url, data):
        return self.c.post(url, json.dumps(data), content_type="application/json")

    def test_login_success(self):
        response = self.send_json('/login/', {'username': 'g123', 'password': 'g123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Succeeded', response.json()['data'])

    def test_login_failed(self):
        response = self.send_json('/login/', {'username': 'g123', 'password': '123g'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Invalid username or password', response.json()['data'])

    def test_create_user(self):
        response = self.send_json('/register/',
                                  {'username': 'username1234', 'password': '1234567890', 'email': 'xu_qq@test.com',
                                   'user_type': UserType.STUDENT})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Succeeded', response.json()['data'])

    def test_create_user_failed(self):
        response = self.send_json('/register/',
                                  {'username': 'username1234', 'password': '1234567890', 'email': 'xu_qq@test.com',
                                   'user_type': 'student===='})
        self.assertEqual(response.json()['data'], 'user_type: "student====" is not a valid choice.')

    def test_decorator_success(self):
        self.send_json('/login/', {'username': 'g123', 'password': 'g123'})
        response = self.c.get('/test/')
        self.assertEqual(response.json()['data'], 'g123')

    def test_decorator_failed(self):
        response = self.c.get('/test/')
        self.assertEqual(response.json()['data'], 'Please login first')
