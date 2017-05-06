# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone_number = PhoneNumberField(blank=True)

'''
Signals used to extend the user model as a one-to-one link
'''

@receiver(post_save, sender=User)
def create_user_borrower(sender, instance, created, **kwargs):
    if created:
        Borrower.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_borrower(sender, instance, **kwargs):
    if instance.borrower.telephone_number is None:
        instance.borrow.telephone_number = ''
    instance.borrower.save()
