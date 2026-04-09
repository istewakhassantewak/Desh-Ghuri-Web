# urls.py

from django.urls import path
from .views import initiate_payment,payment_success,payment_fail,payment_cancel

urlpatterns = [
    path('payment/initiate/<int:package_id>/',initiate_payment, name='initiate_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/fail/', payment_fail, name='payment_fail'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
]
