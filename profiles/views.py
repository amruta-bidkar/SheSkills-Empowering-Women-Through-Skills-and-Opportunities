from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProviderProfileForm, ProviderSkillForm, PortfolioForm
from .models import ProviderProfile, Skill, ProviderSkill


def _provider_profile_or_create(request):
    if request.user.role != 'provider':
        return None, redirect('customer_dashboard')
    profile = ProviderProfile.objects.filter(user=request.user).first()
    if not profile:
        messages.info(request, 'Please create your provider profile first.')
        return None, redirect('create_profile')
    return profile, None


@login_required
def create_profile(request):
    if request.user.role != 'provider':
        return redirect('customer_dashboard')

    profile = ProviderProfile.objects.filter(user=request.user).first()
    if profile:
        return redirect('my_profile')

    if request.method == 'POST':
        form = ProviderProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your profile was created successfully.')
            return redirect('add_skill')
    else:
        form = ProviderProfileForm()

    return render(request, 'profiles/create_profile.html', {'form': form})


@login_required
def my_profile(request):
    profile, error_response = _provider_profile_or_create(request)
    if error_response:
        return error_response

    return render(
        request,
        'profiles/my_profile.html',
        {'profile': profile}
    )


@login_required
def edit_profile(request):
    profile, error_response = _provider_profile_or_create(request)
    if error_response:
        return error_response

    if request.method == 'POST':
        form = ProviderProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('my_profile')
    else:
        form = ProviderProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})


@login_required
def add_skill(request):
    profile, error_response = _provider_profile_or_create(request)
    if error_response:
        return error_response

    if request.method == 'POST':
        form = ProviderSkillForm(request.POST, provider=profile)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            _provider_skill, created = ProviderSkill.objects.get_or_create(
                provider=profile,
                skill=skill
            )
            if created:
                messages.success(request, 'Skill added successfully!')
            else:
                messages.warning(request, 'You have already added this skill.')
            return redirect('my_profile')
    else:
        form = ProviderSkillForm(provider=profile)

    return render(request, 'profiles/add_skill.html', {'form': form})


@login_required
def add_portfolio(request):
    profile, error_response = _provider_profile_or_create(request)
    if error_response:
        return error_response

    if not profile.skills.exists():
        messages.info(
            request,
            'Add at least one skill before uploading portfolio work.'
        )
        return redirect('add_skill')

    if request.method == 'POST':
        form = PortfolioForm(
            request.POST,
            request.FILES,
            provider=profile
        )
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.provider = profile
            portfolio.save()
            messages.success(
                request,
                'Your portfolio work was uploaded successfully!'
            )
            return redirect('my_profile')
    else:
        form = PortfolioForm(provider=profile)

    return render(request, 'profiles/add_portfolio.html', {'form': form})


def provider_detail(request, provider_id):
    provider = get_object_or_404(
        ProviderProfile.objects.select_related('user').prefetch_related(
            'skills__skill',
            'portfolio__skill',
        ),
        id=provider_id
    )
    return render(
        request,
        'profiles/provider_detail.html',
        {'provider': provider}
    )


def marketplace(request):
    skill_query = (request.GET.get('skill') or '').strip()
    location_query = (request.GET.get('location') or '').strip()

    providers = ProviderProfile.objects.select_related('user').prefetch_related(
        'skills__skill',
        'portfolio',
    )

    if skill_query:
        providers = providers.filter(skills__skill__name__icontains=skill_query)
    if location_query:
        providers = providers.filter(location__icontains=location_query)

    providers = providers.distinct()
    skills = Skill.objects.all().order_by('name')

    return render(
        request,
        'profiles/marketplace.html',
        {
            'providers': providers,
            'skills': skills,
            'skill_query': skill_query,
            'location_query': location_query,
        }
    )
