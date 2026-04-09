from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('package-details/<int:package_id>/', views.package_details, name='package-details'),
    
    # Tour Guide Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-package/', views.create_package, name='create-package'),
    path('update-package/<int:package_id>/', views.update_package, name='update-package'),
    path('delete-package/<int:package_id>/', views.delete_package, name='delete-package'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('update-profile-picture/', views.update_profile_picture, name='update-profile-picture'),
    path('remove-booking/<int:booking_id>/', views.remove_booking, name='remove-booking'),

    # Booking Details
    path('order-details/<int:booking_id>/', views.order_details, name='order-details'),
]
