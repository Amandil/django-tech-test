# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):

    # return redirect('/dashboard')

    context = {
        'title': 'Sign In'
    }
    return render(request, 'loans/auth.html', context)

def dashboard(request):
    context = {
        'title': 'Homepage'
    }
    return render(request, 'loans/base_index.html', context)
