# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField

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

class CRNField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(CRNField, self).formfield(**defaults)

class Business(models.Model):
    crn = CRNField(primary_key=True, min_value=0, max_value=99999999, unique=True)
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
