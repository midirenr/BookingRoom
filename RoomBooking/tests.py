from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.http import FileResponse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_200_OK

from .models import Room


class AuthTest(TestCase):
    def test_login(self):
        """
        Тест на status_code
        """
        client = Client()
        response = client.post('/api/v1/auth/login/', {"username": "admin", "password": "admin"})
        self.assertIs(response.status_code, HTTP_200_OK)

    def test_logout(self):
        """
        Тест на status_code
        """
        client = Client()
        response = client.post('/api/v1/auth/logout/')
        self.assertIs(response.status_code, HTTP_200_OK)


class ViewBookingTest(TestCase):
    def test_get_booking(self):
        """
        Тест на status_code
        """
        client = Client()

        response = client.get('/api/v1/booking/view/')
        self.assertIs(response.status_code, HTTP_200_OK)

    def test_post_booking(self):
        """
        Тест на status_code
        """
        client = Client()
        response = client.post('/api/v1/booking/view/', {
            "room": "A1",
            "date_time_start": "2024-03-22T08:17:15",
            "date_time_end": "2024-03-22T08:17:30"
        })
        self.assertIs(response.status_code, HTTP_200_OK)


class CreateBookingTest(TestCase):
    def test_get_create_booking(self):
        """
        Тест на status_code
        """
        client = Client()
        user = User.objects.create(username='TestUser')
        user.set_password('TestUser')
        user.save()
        client.login(username='TestUser', password='TestUser')

        response = client.get('/api/v1/booking/create/')
        client.logout()

        self.assertIs(response.status_code, HTTP_200_OK)

    def test_post_create_booking(self):
        """
        Тест на status_code
        """
        client = Client()
        user = User.objects.create(username='TestUser')
        user.set_password('TestUser')
        user.save()
        client.login(username='TestUser', password='TestUser')
        room = Room()
        room.number = 'A1'
        room.save()

        response = client.post('/api/v1/booking/create/',
                               {
                                   "room": "A1",
                                   "date_time_start": "2024-03-22T08:20:05",
                                   "date_time_end": "2024-03-22T08:21:35",
                                   "purpose": "test"
                               })
        client.logout()
        self.assertIs(response.status_code, HTTP_201_CREATED)


class ReportBookingTest(TestCase):
    def test_get_get_report(self):
        """
        Тест на status_code
        """
        client = Client()
        response = client.get('/api/v1/booking/get_report/')
        self.assertIs(response.status_code, HTTP_200_OK)

    def test_post_get_report(self):
        """
        Тест на получение файла в ответе
        """
        client = Client()
        response = client.post('/api/v1/booking/get_report/',
                               {
                                   "room": "A1",
                                   "date_time_start": "2020-03-22T08:20:05",
                                   "date_time_end": "2030-03-22T08:21:35",
                               })
        client.logout()
        self.assertIs(response.status_code, HTTP_200_OK)
