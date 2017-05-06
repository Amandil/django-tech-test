# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_borrower = models.BooleanField(default=False)
    telephone_number = PhoneNumberField(blank=True)

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
    # Neccessary, cannot throw exception as we are extending User
    if instance.borrower.telephone_number is None:
        instance.borrower.telephone_number = ''
    if str(instance.borrower.telephone_number) == '+NoneNone':
        instance.borrower.telephone_number = ''
    instance.borrower.save()
