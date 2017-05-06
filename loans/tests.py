# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class BorrowerTestCase(TestCase):

    '''
    New 'phone number' field should be valid and optional
    '''
    def test_model_create(self):

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
    def test_telephone_format(self):

        # No extension | Uses PHONENUMBER_DEFAULT_REGION in settings.py
        john = User.objects.create(first_name="John", last_name="Doe")
        john.borrower.telephone_number = '7762 25 4775'
        john.save()

        self.assertEqual(str(john.borrower.telephone_number), '+447762254775')

        # Invalid numbers should not be accepted
        john.borrower.telephone_number = '+00 7762 25 4775 7762 25 4775'
        john.save()

        self.assertEqual(str(john.borrower.telephone_number), '')

        # International numbers should be accepted
        john.borrower.telephone_number = '+40 745 497 778'
        john.save()
        self.assertEqual(str(john.borrower.telephone_number), '+40745497778')

    '''
    Phone number must be unique
    '''
    def test_telephone_duplicate(self):
        john = User.objects.create(username="johndoe", first_name="John", last_name="Doe")
        john.borrower.is_borrower = True
        john.borrower.telephone_number = '+44 7762 25 4775'
        john.save()

        jane = User.objects.create(username="janedoe", first_name="Jane", last_name="Doe")
        jane.borrower.is_borrower = True
        jane.borrower.telephone_number = '+44 7762 25 4775'

        with self.assertRaises(IntegrityError):
            jane.save()

class BusinessTestCase(TestCase):

    '''
    Creating two business owners
    '''
    def setUp(self):

        self.john = User.objects.create(username="johndoe", first_name="John", last_name="Doe")
        self.john.borrower.is_borrower = True
        self.john.borrower.telephone_number = '+44 7762 25 4775'
        self.john.save()

        # self.jane = User.objects.create(username="janedoe", first_name="Jane", last_name="Doe")
        # self.jane.borrower.is_borrower = True
        # self.jane.borrower.telephone_number = '+40 745 497 778'
        # self.jane.save()

    '''
    We must be able to create a business
    '''
    def test_model_create(self):
        acme = Business.objects.create(
            rcn = 09264172,
            owner = self.john.pk,
            name = "ACME Inc.",
            sector = 'Professional Services',
            address_one = '',
            address_two = '',
            city = 'London',
            postcode = 'W8 5EH',
        )

    '''
    Two businesses cannot have the same company number
    '''
    def test_company_number_duplicate(self):
        pass

    '''
    The company number must be added in a valid format
    '''
    def test_company_number_format(self):
        pass

    '''
    The address must be added in a valid format
    '''
    def test_address_format(self):
        pass

    # def test

class LoanTestCase(TestCase):

    def setUp(self):
        pass
