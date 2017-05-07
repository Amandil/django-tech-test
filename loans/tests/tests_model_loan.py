# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from moneyed import Money, GBP
from loans.models import Business, Loan
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date, timedelta

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
            loan_deadline = '2018-02-02',
            reason = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem.'
        )

    '''
    Loan must be between 10000 and 100000
    '''
    def test_loan_amount(self):

        # Too small, should not be valid
        with self.assertRaises(ValidationError):
            loan = Loan.objects.create(
                target_business = self.acme,
                amount = Money(5000, GBP),
                loan_deadline = '2018-02-02',
                reason = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem.'
            )
            loan.full_clean()

        # Too large, should not be valid
        with self.assertRaises(ValidationError):
            loan = Loan.objects.create(
                target_business = self.acme,
                amount = Money(500000, GBP),
                loan_deadline = '2018-02-02',
                reason = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem.'
            )
            loan.full_clean()

    '''
    Loan duration should be between one month and two years (See README.md for assumptions made)
    '''
    def test_loan_duration(self):

        # Too short ammount of time, should not be valid
        with self.assertRaises(ValidationError):
            loan = Loan.objects.create(
                target_business = self.acme,
                amount = Money(50000, GBP),
                loan_deadline = date.today(),
                reason = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem.'
            )
            loan.full_clean()

        # Too long ammount of time, should not be valid
        with self.assertRaises(ValidationError):
            loan = Loan.objects.create(
                target_business = self.acme,
                amount = Money(50000, GBP),
                loan_deadline = '2029-02-02',
                reason = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean porta ligula ac mattis congue. Aenean ut felis sit amet quam auctor cursus. Nulla in ornare sem, non tristique nisi. Sed volutpat rhoncus diam id convallis. Phasellus nec enim at libero scelerisque tempus. In mauris nisl, dictum non varius in, ultrices et lorem.'
            )
            loan.full_clean()
