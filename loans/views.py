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

def registration(request):
    context = {
        'title': 'Register'
    }
    return render(request, 'loans/base_register.html', context)

def dashboard(request):
    context = {
        'title': 'Homepage',
        'loans': [
            {
                'business_name': 'ACME Inc.',
                'amount': '12,000',
                'deadline': '12 Dec 2022',
                'left': '451 days'
            },
            {
                'business_name': 'ACME Inc.',
                'amount': '12,000',
                'deadline': '12 Dec 2022',
                'left': '451 days'
            },
            {
                'business_name': 'ACME Inc.',
                'amount': '12,000',
                'deadline': '12 Dec 2022',
                'left': '451 days'
            },
            {
                'business_name': 'ACME Inc.',
                'amount': '12,000',
                'deadline': '12 Dec 2022',
                'left': '451 days'
            },
            {
                'business_name': 'ACME Inc.',
                'amount': '12,000',
                'deadline': '12 Dec 2022',
                'left': '451 days'
            },
        ]
    }
    return render(request, 'loans/base_index.html', context)
