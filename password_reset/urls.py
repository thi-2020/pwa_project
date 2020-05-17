""" URL Configuration for core auth
"""
from django.urls import path, include
from .views import reset_password_request_token, reset_password_confirm, reset_password_validate_token

app_name = 'password_reset'

urlpatterns = [
    path('validate_token/', reset_password_validate_token, name="reset-password-validate"),
    path('confirm/', reset_password_confirm, name="reset-password-confirm"),
    path('request_reset', reset_password_request_token, name="reset-password-request"),
]
