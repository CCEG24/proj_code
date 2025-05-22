from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.models import User

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # First check if user exists (case-insensitive)
        try:
            user = User.objects.get(username__iexact=username)
            # If user exists, try to authenticate
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('home:index')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, f'Username "{username}" does not exist. Please check your username or register a new account.')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home:index')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        if 'update_email' in request.POST:
            email_form = UserUpdateForm(request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Your email has been updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Your password has been changed!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        email_form = UserUpdateForm(instance=user)
        password_form = CustomPasswordChangeForm(user)
    
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%B %d, %Y'),
        'last_login': user.last_login.strftime('%B %d, %Y %H:%M') if user.last_login else 'Never',
        'is_superuser': user.is_superuser,
        'email_form': email_form,
        'password_form': password_form,
    }
    return render(request, 'accounts/profile.html', context)
