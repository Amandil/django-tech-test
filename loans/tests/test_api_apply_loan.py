import unittest, requests, os

from django.test import TransactionTestCase
from selenium import webdriver

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.test import Client

import time

ENDPOINT = os.environ["LOANS_URL"]
API_ENDPOINT =  ENDPOINT + "/api/v1"

class TestApplyLoanAPI(TransactionTestCase):

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

        self.client.post(API_ENDPOINT + "/user/add",content_type="application/json", data=payload)

        # Logging in
        payload = """{
            "email": "john.smith@acme.com",
            "password": "correct-horse-battery-staple"
        }"""

        self.client.post(API_ENDPOINT + "/user/log_in",content_type="application/json", data=payload)

        # Creating a business
        payload = """{
            "crn": "09264172",
            "business_name": "ACME Inc.",
            "sector": "Retail",
            "address_1": "Building and Number",
            "address_2": "Street",
            "city": "London",
            "postcode": "W8 5EH"
        }"""

        response = self.client.post(API_ENDPOINT + "/business/add",content_type="application/json", data=payload)
        self.assertEqual(200, response.status_code, response.content)

    '''
    We should be able to apply for a loan
    '''
    def test_loan_add(self):

        # Creating a business
        payload = """{
            "crn": "09264172",
            "amount": "50000",
            "deadline": "2018-02-02",
            "reason": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem."
        }"""

        response = self.client.post(API_ENDPOINT + "/loan/add",content_type="application/json", data=payload)
        self.assertEqual(200, response.status_code, response.content)
