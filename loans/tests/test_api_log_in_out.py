import unittest, requests, os

from django.test import TransactionTestCase
from selenium import webdriver

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.test import Client

import time

ENDPOINT = os.environ["LOANS_URL"]
API_ENDPOINT =  ENDPOINT + "/api/v1"

class TestAPILogInOut(TransactionTestCase):

    '''
    Creating the client and a sample user
    '''
    def setUp(self):
        self.client = Client()

        # Creating a user
        payload = """{
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@acme.com",
            "password": "correct-horse-battery-staple",
            "telephone_number": "+44 7765 222 4567"
        }"""

        response = self.client.post(API_ENDPOINT + "/register",content_type="application/json", data=payload)
        self.assertEqual(200, response.status_code)

    '''
    Attempting a log in
    '''
    def test_log_in(self):
        payload = """{
            "email": "john.smith@acme.com",
            "password": "correct-horse-battery-staple"
        }"""

        response = self.client.post(API_ENDPOINT + "/log_in",content_type="application/json", data=payload)
        self.assertEqual(302, response.status_code)

    '''
    Attempting a log in and then log out
    '''
    def test_log_out(self):
        payload = """{
            "email": "john.smith@acme.com",
            "password": "correct-horse-battery-staple"
        }"""

        response = self.client.post(API_ENDPOINT + "/log_in",content_type="application/json", data=payload)
        self.assertEqual(302, response.status_code)

        payload = "{}"
        response = self.client.post(API_ENDPOINT + "/log_out",content_type="application/json", data=payload)
        self.assertEqual(302, response.status_code)
