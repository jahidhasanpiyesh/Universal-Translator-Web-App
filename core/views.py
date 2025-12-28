from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile, TranslationHistory 
import json
from django.http import JsonResponse
from deep_translator import GoogleTranslator

# ল্যাঙ্গুয়েজ লিস্টটি হোমে রেন্ডার করার জন্য
def home(request):
    languages_list = {
        'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic', 'hy': 'Armenian', 'az': 'Azerbaijani',
        'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian',
        'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-CN': 'Chinese (Simplified)',
        'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
        'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French',
        'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati',
        'ht': 'Haitian Creole', 'ha': 'Hausa', 'iw': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong',
        'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish',
        'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh',
        'km': 'Khmer', 'ko': 'Korean', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
        'lt': 'Lithuanian', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
        'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)',
        'ne': 'Nepali', 'no': 'Norwegian', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish',
        'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan',
        'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi',
        'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish',
        'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil',
        'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
        'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish',
        'yo': 'Yoruba', 'zu': 'Zulu'
    }
    return render(request, 'index.html', {'languages': languages_list})

# API যা জাভাস্ক্রিপ্ট থেকে রিকোয়েস্ট গ্রহণ করবে
def translate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_text = data.get('text', '').strip()
            target_lang = data.get('target', 'bn')

            if not user_text:
                return JsonResponse({'translated_text': ''})

            translated = GoogleTranslator(source='auto', target=target_lang).translate(user_text)

            # লগইন করা থাকলে ইতিহাস সেভ হবে
            if request.user.is_authenticated:
                TranslationHistory.objects.create(
                    user=request.user,
                    source_text=user_text,
                    translated_text=translated,
                    target_lang=target_lang
                )

            return JsonResponse({'translated_text': translated})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def signin(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'signup':
            name = request.POST.get('full_name')
            email = request.POST.get('email')
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('re_password')
            
            if pass1 != pass2:
                messages.error(request, "Passwords do not match!")
            elif User.objects.filter(username=email).exists():
                messages.error(request, 'User with this email already exists!')
            else:
                user = User.objects.create_user(username=email, email=email, password=pass1)
                user.first_name = name
                user.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('signin')
                
        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
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
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profile_edit(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        
        if not full_name or not email:
            messages.error(request, 'Full Name and Email are required!')
            return render(request, 'profile_edit.html')

        # পাসওয়ার্ড পরিবর্তন লজিক
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        
        password_changed = False
        if current_pass and new_pass:
            if user.check_password(current_pass):
                user.set_password(new_pass)
                password_changed = True
            else:
                messages.error(request, 'Current password was incorrect!')
                return render(request, 'profile_edit.html')

        # সাধারণ তথ্য আপডেট
        try:
            user.first_name = full_name
            user.email = email
            user.username = email # যেহেতু আপনি ইমেইলকে ইউজারনেম হিসেবে ব্যবহার করছেন
            user.save()
            
            if profile_pic:
                profile.image = profile_pic
            profile.save()

            if password_changed:
                update_session_auth_hash(request, user)
                messages.success(request, 'Profile and Password updated successfully!')
            else:
                messages.success(request, 'Profile updated successfully!')
            
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, 'This email is already in use by another account!')
            return render(request, 'profile_edit.html')

    return render(request, 'profile_edit.html')

def privacy_view(request):
    return render(request, 'privacy.html')

def help_view(request):
    return render(request, 'help.html')

def about_view(request):
    return render(request, 'about.html')