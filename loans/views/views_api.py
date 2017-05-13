# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

def register(request):

    if request.method == 'POST':

        data = request.POST

        try:

            # Generating username
            username = data['first_name'] + "." + data['last_name']
            count = 0
            # .exists() wouldn't work with username for some reason
            while User.objects.filter(username=username).count() is not 0:
                count += 1
                username = data['first_name'] + "." + data['last_name'] + str(count)

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

            # Valiadtion and save
            new_user.full_clean()
            new_user.save()

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
