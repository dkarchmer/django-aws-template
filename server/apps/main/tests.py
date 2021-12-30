#import unittest
import json

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory

from .models import *

user_model = get_user_model()

class MainTestCase(TestCase):
    """
    Fixure includes:
    """
    #fixtures = ['testdb_main.json']

    def setUp(self):
        self.u1 = user_model.objects.create_superuser(username='User1', email='user1@foo.com', password='pass')
        self.u1.is_active = True
        self.u1.save()
        self.u2 = user_model.objects.create_user(username='User2', email='user2@foo.com', password='pass')
        self.u2.is_active = True
        self.u2.save()
        self.u3 = user_model.objects.create_user(username='User3', email='user3@foo.com', password='pass')
        self.u3.is_active = True
        self.u3.save()
        return

    def tearDown(self):
        user_model.objects.all().delete()

    def testPages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.login(email='user1@foo.com', password='pass')
        response = self.client.get('/', {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def testPostContactMessage(self):

        '''
        resp = self.client.post('/api/v1/message', {'name':'M1', 'email':'foo@bar.com',
                                               'phone':'(650)555-1234',
                                               'message':'This is a test'},
                           format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post('/api/v1/message', {'name':'M1', 'email':'foo@bar.com',
                                               'message':'This is another test from same user'},
                           format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post('/api/v1/message', {'name':'M2', 'email':'foo@foo.com',
                                               'message':'This is a test'},
                           format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Nobody should be able to read
        resp = self.client.get('/api/v1/message', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        resp = self.client.get('/api/v1/message/1', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # even if logged in but not staff
        self.client.login(email='user2@foo.com', password='pass')

        resp = self.client.get('/api/v1/message', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        resp = self.client.get('/api/v1/message/1', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

        # SuperUser or Staff can access it
        self.client.login(email='user1@foo.com', password='pass')

        resp = self.client.get('/api/v1/message', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        deserialized = json.loads(resp.content)
        self.assertEqual(deserialized['count'], 3)
        resp = self.client.get('/api/v1/message/1', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.logout()
        '''

