from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from CAuthentication.forms import SignUpForm, UpdateUserForm, ChangePasswordForm


# Create your views here.

def home(request):
    # return render(request, 'test.html')
    return render(request, 'Home/home.html')


def login_page(request):
    print("In loggin in view")
    if request.method == 'POST':
        username = request.POST['UsernameField']
        password = request.POST['passwordField']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('CAuthentication:home')
        else:
            messages.warning(request, "Check your credentials")
            return redirect('CAuthentication:login')
    else:
        return render(request, 'CAuthentication/login.html', {})


def signup_page(request):
    if request.method == 'POST':
        print(request.POST)
        creation_form = SignUpForm(request.POST)
        if creation_form.is_valid():
            creation_form.save()
            username = creation_form.cleaned_data['username']
            password = creation_form.cleaned_data['password1']
            user = authenticate(request, password=password, username=username)
            if user is not None:
                login(request, user)
                messages.success(request, "Created User Successfully!")
                return redirect('CAuthentication:home')
        else:
            messages.warning(request, "An error was encountered, please try again!")
            return redirect('CAuthentication:signup')
    else:
        return render(request, 'CAuthentication/signup.html', {})


def profile(request):
    if request.user.is_authenticated:
        print(request.POST)
        update_form = UpdateUserForm(request.POST or None, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('CAuthentication:profile')
        return render(request, 'CAuthentication/UpdateProfile.html', {'update_form': update_form})
    else:
        messages.warning(request, 'You have to be authenticated to access this page!')
        return redirect('CAuthentication:home')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have logged out successfully!')
        return redirect('CAuthentication:home')
    else:
        messages.warning(request, 'You have to be authenticated to access this page!')
        return redirect('CAuthentication:home')


def change_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print(request.POST)
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Changed password successfully!")
                return redirect('CAuthentication:login')
            else:
                messages.warning(request, 'Check on your passwords!')
                return redirect('CAuthentication:profile')
        else:
            messages.warning(request, 'You have to be authenticated to access this page!')
            return redirect('CAuthentication:home')
    return redirect('CAuthentication:profile')