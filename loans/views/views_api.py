# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json

from loans.models import Business

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
            new_user = User(
                username = username,
                first_name =  data['first_name'],
                last_name =  data['last_name'],
                email =  data['email'],
            )
            new_user.set_password(data['password'])
            new_user.borrower.telephone_number = data['telephone_number']
            new_user.borrower.is_borrower = True

            # Validation and save
            new_user.full_clean()
            new_user.save()

            # Checking if phone number was parsed correctly
            # (Can only be done after the save due to field and user model constraints)
            if len(str(new_user.borrower.telephone_number)) < 1:
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

    data = json.loads(request.body.decode('utf-8'))

    try:
        email = data['email']
        # Looking up username based on email
        username = next(iter(User.objects.filter(email=email)), None).username
        password = data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return JsonResponse({'message': "Invalid username or password " + username}, status=401)


    except KeyError as ke:
        return JsonResponse({'message': str(ke) + " is required"}, status=400)

def log_out(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': "You must be logged in to use this feature"}, status=403)

    logout(request)

    return redirect('index')

def add_business(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': "You must be logged in to use this feature"}, status=403)

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        sector = ""
        if 'Ret' in data['sector']:
            sector = 'RT'
        elif 'Profes' in data['sector']:
            sector = 'PS'
        elif 'Food' in data['sector']:
            sector = 'FD'
        elif 'Enter' in data['sector']:
            sector = 'EN'

        try:
            new_business = Business(
                crn = data['crn'],
                owner = request.user,
                name = data['business_name'],
                sector = sector,
                address_one = data['address_1'],
                address_two = data['address_2'],
                city = data['city'],
                postcode = data['postcode'],
            )
            new_business.full_clean()
            new_business.save()

        except IntegrityError as ie:
            return JsonResponse({'message': str(ie)}, status=400)

        except ValidationError as ve:
            return JsonResponse({'message': str(ve)}, status=400)

        except KeyError as ke:
            return JsonResponse({'message': str(ke) + " is required"}, status=400)

        return JsonResponse({'message': 'Business added'})
    else:
        return JsonResponse({}, status=400)
