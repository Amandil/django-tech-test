from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from loans import views

urlpatterns = [
    # User authentication
    url(r'^$', views.views_ui.index, name='index'),
    url(r'^register$', views.views_ui.registration, name='registration'),
    # Main dashboard
    url(r'^dashboard$', views.views_ui.dashboard, name='dashboard'),
    # Loan application
    url(r'^apply/loan-application/([1-4]{1})/', views.views_ui.loan_application, name='loan_application'),
    url(r'^apply/loan-application/([1-4]{1})/([a-z,A-Z,0-9]{8})$', views.views_ui.loan_application, name='loan_application_crn'),
    # "API"
    url(r'^api/v1/user/add$', views.views_api.register),
    url(r'^api/v1/user/log_in$', views.views_api.log_in),
    url(r'^api/v1/user/log_out$', views.views_api.log_out),
    url(r'^api/v1/business/add$', views.views_api.add_business),
    url(r'^api/v1/loan/add$', views.views_api.add_loan)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
