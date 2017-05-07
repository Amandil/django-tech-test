# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from moneyed import Money, GBP
from djmoney.models.fields import MoneyField,MoneyPatched
from datetime import date

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_borrower = models.BooleanField(default=False)
    telephone_number = PhoneNumberField(blank=True, unique=True)

    def __str__(self):
        return str(self.telephone_number)

'''
Signals used to extend the user model as a one-to-one link
'''

@receiver(post_save, sender=User)
def create_user_borrower(sender, instance, created, **kwargs):
    if created:
        Borrower.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_borrower(sender, instance, **kwargs):
    # Getting rid of null or invalid values
    # We cannot throw exception as we are extending User
    if instance.borrower.telephone_number is None:
        instance.borrower.telephone_number = ''
    if str(instance.borrower.telephone_number) == '+NoneNone':
        instance.borrower.telephone_number = ''
    instance.borrower.save()

class Business(models.Model):
    crn = models.CharField(primary_key=True, max_length=8, unique=True, validators=[MinLengthValidator(8)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    SECTOR_CHOICES = (
        ('RT', 'Retail'),
        ('PS', 'Professional Services'),
        ('FD', 'Food & Drink'),
        ('EN', 'Entertainment')
    )
    sector = models.CharField(max_length=2, choices=SECTOR_CHOICES)
    address_one = models.CharField(max_length=255)
    address_two = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return "(" + str(self.crn) + ") " + self.name

    class Meta:
        verbose_name_plural = "Businesses"

class Loan(models.Model):
    target_business = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = MoneyField(
        max_digits=6,
        decimal_places=0,
        default_currency='GBP',
        validators=[
            MinValueValidator(10000.0),
            MaxValueValidator(100000.0)
        ]
    )
    loan_deadline = models.DateField(default=date.today, blank=False)
    reason = models.TextField()

    def __str__(self):
        time_left = self.loan_deadline - date.today()
        return str(self.target_business) + " - " + str(self.amount) + " - " + str(time_left.days) + " days left"
