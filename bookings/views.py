from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from datetime import datetime
from .models import Packages, TourLocation, PackageHighlights, Transport
from payments.models import Booking

# Create your views here.


def home(request):
    """
    Displays the home page with a list of all tour packages.
    Handles filtering of packages based on location and date provided in GET parameters.
    """
    # Get all packages initially
    packages = Packages.objects.all()
    
    # Get all unique tour locations
    tour_locations = TourLocation.objects.values_list('location', flat=True).distinct()
    
    # Handle filtering
    if request.method == 'GET' and ('location' in request.GET or 'date' in request.GET):
        filter_location = request.GET.get('location', '')
        filter_date = request.GET.get('date', '')
        
        # Apply location filter if provided
        if filter_location:
            packages = packages.filter(location__location=filter_location).distinct()
        
        # Apply date filter if provided
        if filter_date:
            try:
                filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
                packages = packages.filter(
                    start_date__date__lte=filter_date_obj,
                    end_date__date__gte=filter_date_obj
                ).distinct()
            except ValueError:
                messages.error(request, "Invalid date selected. Please choose a valid date.")
    
    context = {
        'packages': packages,
        'tour_locations': tour_locations,
    }
    return render(request, 'index.html', context)




def package_details(request, package_id):
    """
    Displays the detailed view of a single tour package.
    """
    package = get_object_or_404(Packages, id=package_id)
    return render(request, 'package-details.html', {'package': package})

def about_us(request):
    """
    Renders the 'About Us' page.
    """
    team = [
        {
            "name": "Aisha Rahman",
            "role": "Founder & Product Lead",
            "image": "img/team-1.jpg",
            "fallback_image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=600&q=60",
            "linkedin": "#",
            "twitter": "#",
        },
        {
            "name": "Nafis Karim",
            "role": "Head of Operations",
            "image": "img/team-2.jpg",
            "fallback_image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=600&q=60",
            "linkedin": "#",
            "twitter": "#",
        },
        {
            "name": "Farhana Islam",
            "role": "Community Manager",
            "image": "img/team-3.jpg",
            "fallback_image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=60",
            "linkedin": "#",
            "twitter": "#",
        },
        {
            "name": "Rezaul Haque",
            "role": "Travel Experience Designer",
            "image": "img/team-4.jpg",
            "fallback_image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=60",
            "linkedin": "#",
            "twitter": "#",
        },
    ]
    values = [
        {"icon": "fa-earth-asia", "title": "Authentic Experiences", "description": "We design travel that connects people with local stories and culture."},
        {"icon": "fa-people-group", "title": "Community First", "description": "We support local guides and help communities grow through tourism."},
        {"icon": "fa-shield-heart", "title": "Trust & Safety", "description": "Reliable support, verified guides, and transparent bookings for peace of mind."},
    ]
    return render(request, 'about.html', {"team": team, "values": values})

def contact_us(request):
    """
    Renders the 'Contact Us' page.
    """
    contact_info = [
        {"icon": "fa-location-dot", "title": "Office", "detail": "123 Travel Street\nDhaka, Bangladesh"},
        {"icon": "fa-phone", "title": "Phone", "detail": "+880 1234 567890"},
        {"icon": "fa-envelope", "title": "Email", "detail": "hello@deshghuri.com"},
    ]
    social_links = [
        {"name": "Facebook", "icon": "facebook-f", "url": "#", "color": "primary"},
        {"name": "Instagram", "icon": "instagram", "url": "#", "color": "danger"},
        {"name": "YouTube", "icon": "youtube", "url": "#", "color": "danger"},
        {"name": "LinkedIn", "icon": "linkedin-in", "url": "#", "color": "info"},
    ]
    return render(request, 'contact.html', {"contact_info": contact_info, "social_links": social_links})


@login_required
def dashboard(request):
    """
    Displays the user's dashboard.
    The content of the dashboard is customized based on the user's type
    ('tour_guide' or 'traveler').
    For tour guides, it shows their created packages and bookings.
    For travelers, it shows their bookings and featured packages.
    """
    # Common context for all users
    context = {
        "today": datetime.today(),
    }
    
    # Get all unique tour locations
    tour_locations = TourLocation.objects.values_list('location', flat=True).distinct()
    context["tour_locations"] = tour_locations
    
    # Get all unique vehicle types
    transport_vehicles = Transport.objects.values_list('vehicle', flat=True).distinct()
    context["transport_vehicles"] = transport_vehicles
    
    # Check user type and prepare specific context
    if hasattr(request.user, 'user_type'):
        if request.user.user_type == 'tour_guide':
            # Get tour guide profile
            try:
                tour_guide = request.user.guide_profile
                
                # Tour guide specific context
                packages = Packages.objects.filter(tour_guide=tour_guide)
                
                # Get bookings for all packages created by this guide
                bookings = Booking.objects.filter(package__in=packages).select_related('user', 'package', 'package__tour_guide', 'package__tour_guide__user')
                
                # Get user's own bookings (as traveler)
                traveler_bookings = Booking.objects.filter(user=request.user).select_related('package', 'package__tour_guide', 'package__tour_guide__user')
                
                recent_activities = []
                
                context.update({
                    "packages": packages,
                    "bookings": bookings,
                    "traveler_bookings": traveler_bookings,
                    "recent_activities": recent_activities,
                    "guide_profile": tour_guide,
                })
            except:
                # Handle case where guide profile doesn't exist
                context.update({
                    "packages": [],
                    "bookings": [],
                    "traveler_bookings": [],
                    "recent_activities": [],
                    "guide_profile": None,
                    "profile_error": "Please complete your tour guide profile.",
                })
        else:
            # Traveler specific context
            traveler_bookings = Booking.objects.filter(user=request.user).select_related('package', 'package__tour_guide', 'package__tour_guide__user')
            saved_packages = []  # In the future, you can add: SavedPackage.objects.filter(traveler__user=request.user)
            upcoming_trips = traveler_bookings.filter(status='Success').count()  # Count of upcoming bookings
            featured_packages = Packages.objects.all().order_by('-created_at')[:6]  # Get some featured packages
            
            context.update({
                "traveler_bookings": traveler_bookings,
                "saved_packages": saved_packages,
                "upcoming_trips": upcoming_trips,
                "featured_packages": featured_packages,
                "traveler_profile": request.user.traveler_profile if hasattr(request.user, 'traveler_profile') else None,
            })
    
    return render(request, 'dashboard.html', context)

@login_required
def create_package(request):
    """
    Handles the creation of a new tour package.
    This view is restricted to users with the 'tour_guide' user type.
    It processes POST requests containing package details and creates the
    package along with its associated locations, highlights, and transport options.
    """
    # Check if the user is a tour guide
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tour_guide':
        return HttpResponseForbidden("Access denied. You must be a tour guide to access this page.")
    
    # Get the tour guide profile associated with the user
    try:
        tour_guide = request.user.guide_profile
    except:
        return HttpResponseForbidden("You need to complete your tour guide profile first.")
    
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            location_str = request.POST.get('location')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            details = request.POST.get('details')
            complementary = request.POST.get('complementary')
            
            # Create the package without many-to-many fields first
            package = Packages.objects.create(
                title=title,
                main_location=location_str,
                price=price,
                image=image,
                start_date=start_date,
                end_date=end_date,
                details=details,
                complementary=complementary,
                tour_guide=tour_guide
            )
            
            # Handle tour locations
            tour_locations = request.POST.getlist('tour_location[]')
            tour_hotels = request.POST.getlist('tour_hotel[]')
            
            # Dictionary to keep track of locations we've seen
            added_locations = {}
            
            for i in range(len(tour_locations)):
                if tour_locations[i] and i < len(tour_hotels):
                    location_name = tour_locations[i]
                    hotel_name = tour_hotels[i]
                    
                    # Check if this is a location that already exists in the database
                    existing_location = TourLocation.objects.filter(location=location_name, hotel=hotel_name).first()
                    
                    if existing_location:
                        # Use the existing location
                        location = existing_location
                    else:
                        # Create a new location
                        location = TourLocation.objects.create(
                            location=location_name,
                            hotel=hotel_name
                        )
                    
                    # Use location.id as key to avoid duplicates
                    if location.id not in added_locations:
                        package.location.add(location)
                        added_locations[location.id] = True
            
            # Handle package highlights
            highlights = request.POST.getlist('highlight[]')
            added_highlights = {}
            
            for highlight_text in highlights:
                if highlight_text:
                    # Check if highlight already exists
                    existing_highlight = PackageHighlights.objects.filter(highlight=highlight_text).first()
                    
                    if existing_highlight:
                        highlight = existing_highlight
                    else:
                        highlight = PackageHighlights.objects.create(highlight=highlight_text)
                    
                    # Avoid duplicates
                    if highlight.id not in added_highlights:
                        package.highlight.add(highlight)
                        added_highlights[highlight.id] = True
            
            # Handle transportation
            transport_vehicles = request.POST.getlist('transport_vehicle[]')
            transport_descriptions = request.POST.getlist('transport_description[]')
            added_transports = {}
            
            for i in range(len(transport_vehicles)):
                if transport_vehicles[i] and i < len(transport_descriptions):
                    vehicle_name = transport_vehicles[i]
                    description = transport_descriptions[i]
                    
                    # Check if this vehicle already exists
                    existing_transport = Transport.objects.filter(vehicle=vehicle_name).first()
                    
                    if existing_transport:
                        transport = existing_transport
                        # Update description if it's different
                        if transport.description != description and description:
                            transport.description = description
                            transport.save()
                    else:
                        # Create a new transport
                        transport = Transport.objects.create(
                            vehicle=vehicle_name,
                            description=description
                        )
                    
                    # Avoid duplicates
                    if transport.id not in added_transports:
                        package.transport.add(transport)
                        added_transports[transport.id] = True
            
            messages.success(request, 'Package created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating package: {str(e)}')
        
        return redirect('dashboard')
    
    # If not POST, redirect to the dashboard
    return redirect('dashboard')

@login_required
def delete_package(request, package_id):
    """
    Handles the deletion of a specific package.
    Ensures that the user is a tour guide and is the owner of the package
    before allowing deletion.
    """
    # Check if the user is a tour guide
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tour_guide':
        return HttpResponseForbidden("Access denied. You must be a tour guide to access this page.")
    
    # Get the tour guide profile
    try:
        tour_guide = request.user.guide_profile
    except:
        return HttpResponseForbidden("You need to complete your tour guide profile first.")
    
    package = get_object_or_404(Packages, id=package_id)
    
    # Check if the package belongs to the logged-in guide
    if package.tour_guide.user != request.user:
        return HttpResponseForbidden("You cannot delete a package that doesn't belong to you.")
    
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully!')
    
    return redirect('dashboard')

@login_required
def update_package(request, package_id):
    """
    Handles updating an existing tour package.
    This view is restricted to the tour guide who owns the package.
    It processes POST requests with updated package data, including clearing
    and re-adding related many-to-many field entries.
    """
    # Check if the user is a tour guide
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tour_guide':
        return HttpResponseForbidden("Access denied. You must be a tour guide to access this page.")
    
    # Get the tour guide profile
    try:
        tour_guide = request.user.guide_profile
    except:
        return HttpResponseForbidden("You need to complete your tour guide profile first.")
    
    package = get_object_or_404(Packages, id=package_id)
    
    # Check if the package belongs to the logged-in guide
    if package.tour_guide.user != request.user:
        return HttpResponseForbidden("You cannot update a package that doesn't belong to you.")
    
    if request.method == 'POST':
        try:
            # Get form data
            package.title = request.POST.get('title')
            package.main_location = request.POST.get('location')
            package.price = request.POST.get('price')
            if 'image' in request.FILES:
                package.image = request.FILES.get('image')
            package.start_date = request.POST.get('start_date')
            package.end_date = request.POST.get('end_date')
            package.details = request.POST.get('details')
            package.complementary = request.POST.get('complementary')
            
            package.save()
            
            # Handle tour locations (clear existing and add new)
            package.location.clear()
            tour_locations = request.POST.getlist('tour_location[]')
            tour_hotels = request.POST.getlist('tour_hotel[]')
            
            for i in range(len(tour_locations)):
                if tour_locations[i] and i < len(tour_hotels):
                    location = TourLocation.objects.create(
                        location=tour_locations[i],
                        hotel=tour_hotels[i]
                    )
                    package.location.add(location)
            
            # Handle package highlights (clear existing and add new)
            package.highlight.clear()
            highlights = request.POST.getlist('highlight[]')
            for highlight_text in highlights:
                if highlight_text:
                    highlight = PackageHighlights.objects.create(highlight=highlight_text)
                    package.highlight.add(highlight)
            
            messages.success(request, 'Package updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating package: {str(e)}')
        
        return redirect('dashboard')
    
    # If not POST, redirect to the dashboard
    return redirect('dashboard')

@login_required
def update_profile(request):
    """
    Handles updating the user's profile information.
    It updates common user fields (name, phone, address) and also
    updates user-type specific profiles (TourGuideProfile or TravelerProfile).
    """
    if request.method == 'POST':
        # Update user information
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.phone_number = request.POST.get('phone_number')
        request.user.address = request.POST.get('address')
        request.user.save()
        
        # Update type-specific profile
        if hasattr(request.user, 'user_type'):
            if request.user.user_type == 'tour_guide' and hasattr(request.user, 'guide_profile'):
                # Update guide profile
                guide_profile = request.user.guide_profile
                guide_profile.location = request.POST.get('location')
                guide_profile.experience_years = request.POST.get('experience_years')
                guide_profile.languages = request.POST.get('languages')
                guide_profile.expertise = request.POST.get('expertise')
                guide_profile.bio = request.POST.get('bio')
                guide_profile.save()
            elif request.user.user_type == 'traveler' and hasattr(request.user, 'traveler_profile'):
                # Update traveler profile
                traveler_profile = request.user.traveler_profile
                traveler_profile.preferences = request.POST.get('preferences')
                traveler_profile.interests = request.POST.get('interests')
                traveler_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
    
    return redirect('dashboard')

@login_required
def update_profile_picture(request):
    """
    Handles updating the user's profile picture.
    Processes a POST request containing the new image file.
    """
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        request.user.profile_picture = request.FILES.get('profile_picture')
        request.user.save()
        messages.success(request, 'Profile picture updated successfully!')
    
    return redirect('dashboard')

@login_required
def order_details(request, booking_id):
    """
    View to display detailed information about a specific booking.
    
    Ensures that only the traveler who made the booking or the tour guide
    associated with the package can view the details.
    """
    # Get the booking and check permissions
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: only the traveler who booked or the tour guide of the package can view
    is_owner = booking.user == request.user
    is_guide = False
    
    # Check if the user is a tour guide and has access to this booking
    if hasattr(request.user, 'user_type') and request.user.user_type == 'tour_guide':
        try:
            tour_guide = request.user.guide_profile
            if booking.package.tour_guide == tour_guide:
                is_guide = True
        except:
            pass
    
    if not (is_owner or is_guide):
        return HttpResponseForbidden("You don't have permission to view this booking.")
    
    context = {
        'booking': booking,
        'is_owner': is_owner,
        'is_guide': is_guide,
    }
    
    return render(request, 'order_details.html', context)


@login_required
def remove_booking(request,booking_id):
    """
    Deletes a booking record from the database.
    """
    booking=get_object_or_404(Booking,id=booking_id)
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to cancel this booking.")
    if booking.status != 'Pending':
        messages.error(request, "Only pending bookings can be cancelled.")
        return redirect('dashboard')
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('dashboard')
