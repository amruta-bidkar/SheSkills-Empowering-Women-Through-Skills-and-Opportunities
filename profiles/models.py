
# Create your models here.
from django.db import models
from django.conf import settings


class ProviderProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )

    full_name = models.CharField(max_length=100)

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        max_length=500,
        blank=True
    )

    location = models.CharField(
        max_length=150
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProviderSkill(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='providers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('provider', 'skill')

    def __str__(self):
        return f"{self.provider.full_name} - {self.skill.name}"

class Portfolio(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='portfolio'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='portfolio_items'
    )

    title = models.CharField(max_length=150)

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='portfolio/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} - {self.provider.full_name}"