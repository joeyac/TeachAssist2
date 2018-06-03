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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Invalid username or password', response.json()['data'])
