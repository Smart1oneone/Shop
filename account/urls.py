from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('email-verification/, views.email_verification', name='email_verification'),

]