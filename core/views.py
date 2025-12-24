from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile

# Create your views here.

def home(request):
    return render(request, 'index.html')

# Signin view handling both signup and login
def signin(request):
    if request.method == "POST":

        # Determine which form was submitted
        form_type = request.POST.get('form_type')

        # --- SIGNUP LOGIC ---
        if form_type == 'signup':
            name = request.POST.get('full_name')
            email = request.POST.get('email')
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('re_password')

            # Validation checks
            if pass1 != pass2:
                messages.error(request, "Passwords do not match!")
            elif User.objects.filter(username=email).exists():
                messages.error(request, 'User with this email already exists!')
            else:
                # Password match and user doesn't exist, create user
                user = User.objects.create_user(
                    username=email, email=email, password=pass1)
                user.first_name = name
                user.save()
                messages.success(
                    request, 'Account created successfully! Please login.')
                return redirect('signin')

        # --- LOGIN LOGIC ---
        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Django username field is email in this case
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password!')

    return render(request, 'signin.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Logged out succesfully!')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profile_edit(request):
    user = request.user
    # OneToOneField relationship to get or create user profile
    # This assumes UserProfile model has a OneToOneField to User
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')

        if not full_name or not email:
            messages.error(request, 'Full Name and Email are required!')
            return render(request, 'profile_edit.html')

        # Update User fields
        user.first_name = full_name
        user.email = email
        user.username = email 

        # Update profile picture if provided
        if profile_pic:
            profile.image = profile_pic
            profile.save() # Save profile changes

        # Handle password change if fields are filled
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')

        if current_pass and new_pass:
            if user.check_password(current_pass):
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Profile and Password updated successfully!')
            else:
                messages.error(request, 'Current password was incorrect!')
                return render(request, 'profile_edit.html')
        else:
            try:
                user.save() 
                messages.success(request, 'Profile updated successfully!')
            except Exception as e:
                messages.error(request, 'This email/username is already in use!')
                return render(request, 'profile_edit.html')

        return redirect('profile')

    return render(request, 'profile_edit.html')