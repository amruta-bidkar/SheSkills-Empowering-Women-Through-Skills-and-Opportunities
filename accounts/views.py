from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.models import ProviderProfile, Skill
from .forms import RegisterForm


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.user.is_authenticated:
        if request.user.role == 'provider':
            return redirect('provider_dashboard')
        return redirect('customer_dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Registration successful! Welcome to SheSkills.'
            )
            login(request, user)
            if user.role == 'provider':
                return redirect('provider_dashboard')
            return redirect('customer_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.role == 'provider':
            return redirect('provider_dashboard')
        return redirect('customer_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            if user.role == 'provider':
                return redirect('provider_dashboard')
            return redirect('customer_dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def provider_dashboard(request):
    if request.user.role != 'provider':
        return redirect('customer_dashboard')

    profile = ProviderProfile.objects.filter(user=request.user).first()
    return render(
        request,
        'accounts/provider_dashboard.html',
        {'profile': profile}
    )


@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('provider_dashboard')

    providers = (
        ProviderProfile.objects
        .select_related('user')
        .prefetch_related('skills__skill', 'portfolio')
        .order_by('-is_verified', '-created_at')[:6]
    )
    skills = Skill.objects.all().order_by('name')

    return render(
        request,
        'accounts/customer_dashboard.html',
        {
            'providers': providers,
            'skills': skills,
        }
    )
