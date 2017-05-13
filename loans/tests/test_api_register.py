import unittest, requests, os

from django.test import TransactionTestCase
from selenium import webdriver

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.test import Client

import time

ENDPOINT = os.environ['LOANS_URL']
API_ENDPOINT =  ENDPOINT + "/api/v1"

class TestAPIRegistration(TransactionTestCase):

    '''
    Creating the client
    '''
    def setUp(self):
        self.client = Client()

    '''
    "Happy" registration scenario
    '''
    def test_register(self):

        # Making the request
        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@acme.com',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 222 4567'
        }
        # response = requests.post(API_ENDPOINT + "/register", cookies=self.cookies, headers=self.headers, data=payload)
        response = self.client.post(API_ENDPOINT + "/register", payload)

        # Response must be OK
        self.assertEqual(200, response.status_code)

        # User must have been created
        user = next(iter(User.objects.filter(email='john.smith@acme.com')), None)

        self.assertNotEqual(None, user)

        # User must be a borrower and have a phone number
        self.assertTrue(user.borrower.is_borrower)
        self.assertEqual('+4477652224567', user.borrower.telephone_number)

    '''
    Must only support POST
    '''
    def test_http_method(self):
        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@acme.com',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 222 4567'
        }

        response = self.client.get(API_ENDPOINT + "/register", payload)
        self.assertEqual(400, response.status_code)

        with self.assertRaises(ObjectDoesNotExist):
            new_user = User.objects.get(email='john.smith@acme.com')

    '''
    Users must be unique
    '''
    def test_integrity(self):

        # Creating reference user
        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@acme.com',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 222 4567'
        }

        response = self.client.post(API_ENDPOINT + "/register", payload)
        # Making sure that worked
        self.assertEqual(200, response.status_code)

        # Creating user with same email address
        payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.smith@acme.com',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 123 4567'
        }

        response = self.client.post(API_ENDPOINT + "/register", payload)
        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in response.json()['message'])

        # Creating user with same name but different email
        # This validates if the username is generated correctly
        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'smithj@acme.com',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 222 4567'
        }

        response = self.client.post(API_ENDPOINT + "/register", payload)
        self.assertEqual(200, response.status_code)

        # Creating user without a phone number
        payload = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@acme.com',
            'password': 'correct-horse-battery-staple'
        }

        response = self.client.post(API_ENDPOINT + "/register", payload)
        self.assertEqual(400, response.status_code)
        self.assertTrue('telephone' in response.json()['message'])

    '''
    Data must be valid
    '''
    def test_validation(self):
        # Invalid email
        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 222 4567'
        }

        response = self.client.post(API_ENDPOINT + "/register", payload)
        self.assertEqual(400, response.status_code)

        # Invalid phone number
        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@acme.com',
            'password': 'correct-horse-battery-staple',
            'telephone_number': '+44 7765 222 4567 123 123 14 123 123'
        }

        response = self.client.post(API_ENDPOINT + "/register", payload)
        self.assertEqual(400, response.status_code)
