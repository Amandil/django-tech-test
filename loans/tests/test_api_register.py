import unittest, requests, os

from django.test import TestCase
from selenium import webdriver

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

ENDPOINT = os.environ['LOANS_URL']
API_ENDPOINT =  ENDPOINT + "/api/v1"

class TestAPIRegistration(TestCase):

    '''
    Starting a new session with Selenium in order to grab a CSRF token
    '''
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get(ENDPOINT + "/")

        csrf_token =  self.driver.get_cookie('csrftoken')['value']

        self.headers = {
            'X-CSRFToken': csrf_token
        }
        self.cookies = {
            'csrftoken': csrf_token
        }

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
        response = requests.post(API_ENDPOINT + "/register", cookies=self.cookies, headers=self.headers, data=payload)

        # Response must be OK
        self.assertEqual(200, response.status_code)

        # User must have been created
        new_user = User.objects.get(email='john.smith@acme.com')

        self.assertNotEqual(new_user, None)

        # User must be a borrower and have a phone number

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

        response = requests.get(API_ENDPOINT + "/register", cookies=self.cookies, headers=self.headers, data=payload)
        self.assertEqual(400, response.status_code)

        with self.assertRaises(ObjectDoesNotExist):
            new_user = User.objects.get(email='john.smith@acme.com')

    '''
    Users must be unique
    '''
    def test_integrity(self):
        pass

    '''
    Data must be valid
    '''
    def test_validation(self):
        pass
