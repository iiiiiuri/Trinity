from django.shortcuts import render, redirect
from django.contrib import messages
from readerAfd.models import UserProfile
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                userProfile = UserProfile.objects.get(user=user)
                if userProfile.empresa is not None:
                    auth_login(request, user)
                    return redirect('fileData')
                else:
                    auth_login(request, user)
                    return redirect('fileupload')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login') 

    return render(request, 'readerAfd/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login') 


def register(request):
    if request.method == 'POST':
        name = request.POST['nome']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        
        if not UserProfile.objects.filter(user=user).exists():
            user_profile = UserProfile.objects.create(user=user, name=name)
            user_profile.save()

        return redirect('login')

    return render(request, 'readerAfd/register.html')