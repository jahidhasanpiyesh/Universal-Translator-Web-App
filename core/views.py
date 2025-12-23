from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'signin.html')

def profile(request):
    return render(request, 'profile.html')