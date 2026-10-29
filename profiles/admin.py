from django.contrib import admin
from .models import ProviderProfile, Skill, ProviderSkill, Portfolio


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'location',
        'experience',
        'is_verified',
    )
    list_filter = (
        'is_verified',
        'location',
    )
    search_fields = (
        'full_name',
        'location',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProviderSkill)
class ProviderSkillAdmin(admin.ModelAdmin):
    list_display = ('provider', 'skill', 'created_at')
    list_filter = ('skill',)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'skill', 'created_at')
    list_filter = ('skill',)
