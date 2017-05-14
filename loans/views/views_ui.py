# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from loans.models import Loan, Business

def index(request):
    if not request.user.is_authenticated:
        context = {
            'title': 'Sign In'
        }
        return render(request, 'loans/auth.html', context)
    else:
        return redirect('/dashboard')

def registration(request):
    context = {
        'title': 'Register'
    }
    return render(request, 'loans/base_register.html', context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')

    # Finding all of the current user's businesses
    businesses = Business.objects.filter(owner=request.user)

    loans = []

    for business in businesses:
        loans_business = Loan.objects.filter(target_business=business)
        loans += loans_business

    context = {
        'title': 'Homepage',
        'loans': loans
    }
    return render(request, 'loans/base_index.html', context)

def loan_application(request, step, crn=""):
    if not request.user.is_authenticated:
        return redirect('/')

    if step == "1":

        # Retrieving all of the curent user's businesses
        businesses = Business.objects.filter(owner=request.user)

        context = {
            'title': 'Loan Application - Step 1',
            'businesses': businesses
        }
        return render(request, 'loans/base_apply_select_business.html', context)

    elif step == "2":
        context = {
            'title': 'Loan Application - Add Business'
        }
        return render(request, 'loans/base_apply_add_business.html', context)

    elif step == "3":
        context = {
            'title': 'Loan Application - Step 2',
            'crn': crn
        }
        return render(request, 'loans/base_apply_choose_loan.html', context)

    elif step == "4":
        context = {
            'title': 'Loan Application - Success'
        }
        return render(request, 'loans/base_apply_success.html', context)
    # else:
        # Never gonna happen (404)
