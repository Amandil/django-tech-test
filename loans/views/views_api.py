# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

import json

def register(request):

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        try:

            # Generating username
            username = data['first_name'] + "." + data['last_name']
            count = 0
            # .exists() wouldn't work with username for some reason
            while User.objects.filter(username=username).count() is not 0:
                count += 1
                username = data['first_name'] + "." + data['last_name'] + str(count)

            # Ensuring that email is unique because Django
            # couldn't handle something so basic out of the box
            email = next(iter(User.objects.filter(email=data['email'])), None)
            if email is not None:
                raise IntegrityError("\"email\" must be unique")

            # Creating the object
            new_user = User.objects.create(
                username = username,
                first_name =  data['first_name'],
                last_name =  data['last_name'],
                email =  data['email'],
                password =  data['password'],
            )
            new_user.borrower.telephone_number = data['telephone_number']
            new_user.borrower.is_borrower = True

            # Validation and save
            new_user.full_clean()
            new_user.save()

            # Checking if phone number was parsed correctly
            # (Can only be done after the save due to field and user model constraints)
            if len(str(new_user.borrower.telephone_number)) < 1:
                new_user.delete()
                raise ValidationError({'message': 'Phone number is not valid: ' + data['telephone_number']})

        except IntegrityError as ie:
            return JsonResponse({'message': str(ie)}, status=400)

        except ValidationError as ve:
            return JsonResponse({'message': str(ve)}, status=400)

        except KeyError as ke:
            return JsonResponse({'message': str(ke) + " is required"}, status=400)

        return JsonResponse({'message': 'User created'})
    else:
        return JsonResponse({}, status=400)

def log_in(request):
    pass
