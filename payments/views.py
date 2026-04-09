# views.py

import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from bookings.models import Packages  # adjust if needed

@login_required
def initiate_payment(request, package_id):
    package = get_object_or_404(Packages, id=package_id)
    
    # Get guest count from request
    try:
        guest_count = max(1, int(request.GET.get('guest_count', 1)))
    except (TypeError, ValueError):
        guest_count = 1
    
    # Calculate total amount
    total_amount = package.price * guest_count
    
    booking = Booking.objects.create(
        user=request.user,
        package=package,
        guest_count=guest_count,
        amount=total_amount,
        status='Pending'
    )
    
    data = {
        'store_id': settings.SSL_COMMERZ_STORE_ID,
        'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
        'total_amount': total_amount,
        'currency': "BDT",
        'tran_id': f"BOOKING{booking.id}",
        'success_url': settings.SSL_SUCCESS_URL,
        'fail_url': settings.SSL_FAIL_URL,
        'cancel_url': settings.SSL_CANCEL_URL,
        'cus_name': request.user.first_name,
        'cus_email': request.user.email,
        'cus_phone': request.user.phone_number,
        'cus_add1': request.user.address or 'Dhaka',
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'product_name': package.title,
        'product_category': "Tour",
        'product_profile': "general",
        'shipping_method': 'NO',  # ✅ Add this line

    }

    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php" if settings.SSL_COMMERZ_SANDBOX_MODE else "https://securepay.sslcommerz.com/gwprocess/v4/api.php"
    
    try:
        response = requests.post(url, data=data, timeout=30)
        response_data = response.json()
    except Exception:
        messages.error(request, "Payment gateway is currently unavailable. Please try again.")
        return redirect('package-details', package_id=package.id)

    if response_data['status'] == 'SUCCESS':
        return redirect(response_data['GatewayPageURL'])
    else:
        messages.error(request, "Failed to initiate payment. Please try again.")
        return redirect('package-details', package_id=package.id)


@csrf_exempt
def payment_success(request):
    data = request.POST
    tran_id = data.get('tran_id')
    status = data.get('status')
    
    booking_id = tran_id.replace("BOOKING", "")
    booking = get_object_or_404(Booking, id=booking_id)
    
    if status == 'VALID':
        booking.status = 'Success'
        booking.transaction_id = tran_id
        booking.save()
    
    return render(request, 'success.html', {'booking': booking})


@csrf_exempt
def payment_fail(request):
    data = request.POST
    tran_id = data.get('tran_id')
    booking_id = tran_id.replace("BOOKING", "")
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Failed'
    booking.save()
    return render(request, 'fail.html', {'booking': booking})


@csrf_exempt
def payment_cancel(request):
    return render(request, 'cancel.html')
