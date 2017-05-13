# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from django.contrib.auth.models import User

def register(request):

    if request.method == 'POST':
        return JsonResponse({})
    else:
        return JsonResponse({}, status=400)

def log_in(request):
    pass
