# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User

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
        john.borrower.telephone_number = '+44 7762 25 4775'
        self.assertEqual(str(john.borrower.telephone_number), '+447762254775')

        john.save()


    '''
    Only valid phone numbers should be accepted
    '''
    def test_valid_telephone(self):

        # No extension | Uses PHONENUMBER_DEFAULT_REGION in settings.py
        john = User.objects.create(first_name="John", last_name="Doe")
        john.borrower.telephone_number = '7762 25 4775'

        self.assertEqual(str(john.borrower.telephone_number), '+447762254775')

        # Invalid number
        john.borrower.telephone_number = '+00 7762 25 4775 7762 25 4775'
        john.save()

        self.assertEqual(str(john.borrower.telephone_number), '')

class BusinessTestCase(TestCase):

    def setUp(self):
        pass

class LoanTestCase(TestCase):

    def setUp(self):
        pass
