from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import CustomUser, Traveler, TourGuide

from django.contrib.auth import authenticate, login as auth_login


def register(request):
    """
    Handles user registration for both Travelers and Tour Guides.

    For POST requests, it processes the registration form data. It determines the
    user type ('traveler' or 'tour_guide') from the form.

    For a 'traveler':
    - Validates that the passwords match.
    - Checks if a user with the given email already exists.
    - Creates a new CustomUser instance with user_type='traveler'.
    - Creates an associated Traveler profile.
    - Logs the new user in and redirects to the homepage.

    For a 'tour_guide':
    - Validates that the passwords match.
    - Checks if a user with the given email already exists.
    - Creates a new CustomUser instance with user_type='tour_guide'.
    - Creates an associated TourGuide profile with location, experience, and bio.
    - Logs the new user in and redirects to the homepage.

    Handles exceptions during the process and displays error messages.
    For GET requests, it simply renders the registration page.
    """
    if request.method == 'POST':
        # Check if it's a traveler registration
        if request.POST.get('user_type') == 'traveler':
            # Check if passwords match first
            if request.POST.get('touristPassword') != request.POST.get('touristConfirmPassword'):
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')
                
            # Create a new user with the traveler user type
            try:
                email = (request.POST.get('touristEmail') or '').strip().lower()
                if not email:
                    messages.error(request, "Email is required.")
                    return render(request, 'register.html')
                
                # Check if email already exists
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "A user with that email already exists.")
                    return render(request, 'register.html')
                
                user = CustomUser.objects.create_user(
                    email=email,
                    password=request.POST.get('touristPassword'),
                    username=email.split('@')[0],
                    first_name=request.POST.get('touristFirstName', ''),
                    last_name=request.POST.get('touristLastName', ''),
                    phone_number=request.POST.get('touristPhone', ''),
                    user_type='traveler'
                )
                Traveler.objects.create(user=user)
                
                # Log the user in
                auth_login(request, user)
                messages.success(request, "Registration successful! Welcome to Pac-and-Go.")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
        elif request.POST.get('user_type') == 'tour_guide':
            # Check if passwords match first
            if request.POST.get('guidePassword') != request.POST.get('guideConfirmPassword'):
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')
                
            try:
                email = (request.POST.get('guideEmail') or '').strip().lower()
                if not email:
                    messages.error(request, "Email is required.")
                    return render(request, 'register.html')
                
                # Check if email already exists
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "A user with that email already exists.")
                    return render(request, 'register.html')
                
                # Create a new user with the tour guide user type
                user = CustomUser.objects.create_user(
                    email=email,
                    password=request.POST.get('guidePassword'),
                    username=email.split('@')[0],
                    first_name=request.POST.get('guideFirstName', ''),
                    last_name=request.POST.get('guideLastName', ''),
                    phone_number=request.POST.get('guidePhone', ''),
                    user_type='tour_guide'
                )
                
                # Convert experience to int with default if there's a problem
                try:
                    experience_years = int(request.POST.get('guideExperience', 0))
                except (ValueError, TypeError):
                    experience_years = 0
                
                # Create the tour guide profile
                TourGuide.objects.create(
                    user=user,
                    location=request.POST.get('guideLocation', ''),
                    experience_years=experience_years,
                    bio=request.POST.get('guideBio', '')
                )
                
                # Log the user in
                auth_login(request, user)
                messages.success(request, "Registration successful! Welcome to Pac-and-Go.")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            messages.error(request, "Invalid user type selected.")
    
    # For GET requests, just render the template
    return render(request, 'register.html')




def  handle_login(request):
    """
    Handles user authentication and login.

    For POST requests, it attempts to authenticate the user using the provided
    email and password.
    - If authentication is successful, the user is logged in, and they are
      redirected to the 'home' page.
    - If authentication fails, an error message is displayed, and the user is
      redirected back to the 'login' page.

    For GET requests, it renders the login page.
    """
    if request.method ==  "POST":
        data = request.POST

        email = (data.get('email') or '').strip().lower()
        password = data.get('password')
        selected_role = data.get('role')  # 'traveler' or 'tour_guide'
        next_url = request.GET.get('next') or request.POST.get('next')

        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            if selected_role and selected_role != user.user_type:
                messages.warning(request, f"Logged in as {user.user_type.replace('_', ' ').title()}.")
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')
    return render(request, 'login.html', {'next': request.GET.get('next', '')})


def handlelogout(request):
    """
    Logs the current user out of the application.

    This view logs out the user who made the request and then redirects them
    to the 'home' page.
    """
    logout(request)
    return redirect('home')