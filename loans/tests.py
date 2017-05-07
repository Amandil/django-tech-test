# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from moneyed import Money, GBP
from .models import Business, Loan

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
            crn = '09264172',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )
        acme.full_clean()

    '''
    Two businesses cannot have the same company number
    '''
    def test_company_number_duplicate(self):
        acme = Business.objects.create(
            crn = '09264172',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )
        acme.full_clean()

        with self.assertRaises(IntegrityError):
            duplicate = Business.objects.create(
                crn = '09264172',
                owner = self.john,
                name = "ACME Duplicate Inc.",
                sector = 'PS',
                address_one = 'Building and Number',
                address_two = 'Street',
                city = 'Manchester',
                postcode = 'M14 5SZ',
            )


    '''
    The company number must be added in a valid format
    '''
    def test_company_number_format(self):

        # 8 character number should be accepted
        acme = Business.objects.create(
            crn = '09264172',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )

        acme.full_clean()

        # > 8 characters should not be accepted
        acme = Business.objects.create(
            crn = '09264172123123',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )

        with self.assertRaises(ValidationError):
            acme.full_clean()

        # < 8 characters should not be accepted
        acme = Business.objects.create(
            crn = '0926',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )

        with self.assertRaises(ValidationError):
            acme.full_clean()

    '''
    The address must be added in a valid format
    '''
    def test_address_format(self):
        pass


class LoanTestCase(TestCase):

    def setUp(self):

        # We need a business owner
        self.john = User.objects.create(username="johndoe", first_name="John", last_name="Doe")
        self.john.borrower.is_borrower = True
        self.john.borrower.telephone_number = '+44 7762 25 4775'
        self.john.save()

        # Then we need a business
        self.acme = Business.objects.create(
            crn = '09264172',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )
        self.acme.full_clean()

    '''
    We must be able to create a loan
    '''
    def test_create(self):
        Loan.objects.create(
            target_business = self.acme,
            amount = Money(20000, GBP),
            loan_deadline = '2029-02-02',
            reason = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem.'
        )
