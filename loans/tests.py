# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Borrower
from phonenumber_field.modelfields import PhoneNumberField

class BorrowerTestCase(TestCase):

    def setUp(self):
        pass

    '''
    New 'phone number' field should be valid and optional
    '''
    def test_create(self):

        john = User.objects.create(first_name="John", last_name="Doe")

        # If we don't set phone number, it should be an empty string
        self.assertEqual(str(john.borrower.telephone_number), '')

        # If we do set phone number, it should not be an empty string
        john.borrower.telephone_number = '+41 52 424 2424'
        self.assertEqual(str(john.borrower.telephone_number), '+41524242424')


    def test_valid_telephone(self):
        pass

class BusinessTestCase(TestCase):

    def setUp(self):
        pass

class LoanTestCase(TestCase):

    def setUp(self):
        pass
