from django import forms
from django.core.exceptions import ValidationError
from .models import ProviderProfile, ProviderSkill, Portfolio, Skill


MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}


def validate_uploaded_image(image):
    if not image:
        return
    name = getattr(image, 'name', '') or ''
    extension = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    if extension and extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            'Please upload a JPG, PNG, WEBP, or GIF image.'
        )
    size = getattr(image, 'size', None)
    if size and size > MAX_IMAGE_SIZE:
        raise ValidationError('Image must be 5MB or smaller.')


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = [
            'full_name',
            'profile_photo',
            'bio',
            'location',
            'experience',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your full name'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'City or area'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell customers about yourself and your skills...'
            }),
            'experience': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        validate_uploaded_image(photo)
        return photo


class ProviderSkillForm(forms.ModelForm):
    class Meta:
        model = ProviderSkill
        fields = ['skill']

    def __init__(self, *args, provider=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Skill.objects.all().order_by('name')
        if provider is not None:
            queryset = queryset.exclude(providers__provider=provider)
        self.fields['skill'].queryset = queryset
        self.fields['skill'].empty_label = 'Select a skill'


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            'skill',
            'title',
            'description',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Name this piece of work'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }

    def __init__(self, *args, provider=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Skill.objects.all().order_by('name')
        if provider is not None:
            queryset = Skill.objects.filter(
                providers__provider=provider
            ).distinct().order_by('name')
        self.fields['skill'].queryset = queryset
        self.fields['skill'].empty_label = 'Select a skill'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        validate_uploaded_image(image)
        return image
