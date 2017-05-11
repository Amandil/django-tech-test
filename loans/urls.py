from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # User authentication
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.registration, name='registration'),
    # Main dashboard
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    # Loan application
    url(r'^apply/loan-application/([1-4]{1})/', views.loan_application, name='loan_application'),
    url(r'^apply/loan-application/([1-4]{1})/([a-z,A-Z,0-9]{8})$', views.loan_application, name='loan_application_crn'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
