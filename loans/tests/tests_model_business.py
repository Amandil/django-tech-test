# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from loans.models import Business

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

        # First address field must have some characters
        acme = Business.objects.create(
            crn = '09260926',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = '',
            address_two = 'Street',
            city = 'London',
            postcode = 'W8 5EH',
        )
        with self.assertRaises(ValidationError):
            acme.full_clean()

        # Second address field can be empty
        acme = Business.objects.create(
            crn = '09260927',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = '',
            city = 'London',
            postcode = 'W8 5EH',
        )
        acme.full_clean()

        # Postcode must be valid
        acme = Business.objects.create(
            crn = '09260928',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = '',
            city = 'London',
            postcode = 'INVALID POSTCODE',
        )
        with self.assertRaises(ValidationError):
            acme.full_clean()

        acme = Business.objects.create(
            crn = '09260929',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = '',
            city = 'London',
            postcode = ' 2NP',
        )
        with self.assertRaises(ValidationError):
            acme.full_clean()

        acme = Business.objects.create(
            crn = '09260930',
            owner = self.john,
            name = "ACME Inc.",
            sector = 'PS',
            address_one = 'Building and Number',
            address_two = '',
            city = 'London',
            postcode = 'M145S',
        )
        with self.assertRaises(ValidationError):
            acme.full_clean()
