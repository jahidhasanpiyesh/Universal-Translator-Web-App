from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    return render(request, 'index.html')


def signin(request):
    if request.method == "POST":
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
                # Password match korle account create hobe
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

            # Django username field e ekhon email ache
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password!')

    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out succesfully!')
    return redirect('home')
def profile(request):
    return render(request, 'profile.html')


def profile_edit(request):
    return render(request, 'profile_edit.html')
