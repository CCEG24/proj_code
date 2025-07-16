from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UsernameUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import EmailVerificationCode
from .forms import RequestVerificationCodeForm, VerifyCodeForm
import random
from .forms import UpdateEmailForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug information
        print(f"Login attempt - Username: '{username}', Length: {len(username)}")
        print(f"Username characters: {[ord(c) for c in username]}")
        
        # First check if user exists (case-insensitive)
        try:
            user = User.objects.get(username__iexact=username)
            print(f"Found user: '{user.username}', Length: {len(user.username)}")
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

def send_verification_code_view(request):
    if request.method == 'POST':
        user = request.user
        code = f"{random.randint(100000, 999999)}"
        EmailVerificationCode.objects.create(user=user, code=code)
        send_mail(
            'Your Verification Code',
            f'Your verification code is: {code}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(request, 'Verification code sent to your email!')
        return redirect('accounts:profile')
    return redirect('accounts:profile')

def verify_code_view(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            match = EmailVerificationCode.objects.filter(user=request.user, code=code, is_used=False).order_by('-created_at').first()
            if match:
                match.is_used = True
                match.save()
                # Set user as verified
                profile = request.user.profile
                profile.is_email_verified = True
                profile.save()
                messages.success(request, 'Email verified successfully!')
            else:
                messages.error(request, 'Invalid or expired code.')
        else:
            messages.error(request, 'Please enter a valid code.')
        return redirect('accounts:profile')
    return redirect('accounts:profile')

@login_required
def profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        if 'update_username' in request.POST:
            username_form = UsernameUpdateForm(request.POST, instance=user)
            password_form = CustomPasswordChangeForm(user)
            email_form = UpdateEmailForm(instance=user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Your username has been updated!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user, request.POST)
            username_form = UsernameUpdateForm(instance=user)
            email_form = UpdateEmailForm(instance=user)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Your password has been changed!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'update_email' in request.POST:
            email_form = UpdateEmailForm(request.POST, instance=user)
            username_form = UsernameUpdateForm(instance=user)
            password_form = CustomPasswordChangeForm(user)
            old_email = user.email
            if email_form.is_valid():
                updated_user = email_form.save(commit=False)
                if updated_user.email != old_email:
                    updated_user.profile.is_email_verified = False
                    updated_user.profile.save()
                    messages.info(request, 'Email changed. Please verify your new email address.')
                updated_user.save()
                messages.success(request, 'Your email has been updated!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        username_form = UsernameUpdateForm(instance=user)
        password_form = CustomPasswordChangeForm(user)
        email_form = UpdateEmailForm(instance=user)
    request_code_form = RequestVerificationCodeForm()
    verify_code_form = VerifyCodeForm()
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%B %d, %Y'),
        'last_login': user.last_login.strftime('%B %d, %Y %H:%M') if user.last_login else 'Never',
        'is_superuser': user.is_superuser,
        'username_form': username_form,
        'password_form': password_form,
        'email_form': email_form,
        'request_code_form': request_code_form,
        'verify_code_form': verify_code_form,
    }
    return render(request, 'accounts/profile.html', context)
