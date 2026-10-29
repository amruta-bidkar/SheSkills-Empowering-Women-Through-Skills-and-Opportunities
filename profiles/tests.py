from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from accounts.models import User
from .models import ProviderProfile, Skill, ProviderSkill, Portfolio


def make_test_image(name='work.png'):
    buffer = BytesIO()
    Image.new('RGB', (20, 20), color=(200, 80, 120)).save(buffer, format='PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


class ProfileWorkflowTests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name='Tailoring')
        self.provider = User.objects.create_user(
            username='provider1',
            password='StrongPass123!',
            role=User.PROVIDER,
            phone='9991112222',
        )
        self.customer = User.objects.create_user(
            username='customer1',
            password='StrongPass123!',
            role=User.CUSTOMER,
        )

    def test_provider_creates_one_profile(self):
        self.client.login(username='provider1', password='StrongPass123!')
        response = self.client.post(reverse('create_profile'), {
            'full_name': 'Priya Sharma',
            'bio': 'Home tailor',
            'location': 'Hingoli',
            'experience': 5,
        })
        self.assertRedirects(response, reverse('add_skill'))
        self.assertEqual(ProviderProfile.objects.filter(user=self.provider).count(), 1)

        second = self.client.get(reverse('create_profile'))
        self.assertRedirects(second, reverse('my_profile'))

    def test_customer_cannot_create_profile(self):
        self.client.login(username='customer1', password='StrongPass123!')
        response = self.client.get(reverse('create_profile'))
        self.assertRedirects(response, reverse('customer_dashboard'))

    def test_add_skill_does_not_duplicate(self):
        profile = ProviderProfile.objects.create(
            user=self.provider,
            full_name='Priya Sharma',
            location='Hingoli',
            experience=4,
        )
        self.client.login(username='provider1', password='StrongPass123!')
        self.client.post(reverse('add_skill'), {'skill': self.skill.id})
        self.client.post(reverse('add_skill'), {'skill': self.skill.id})
        self.assertEqual(
            ProviderSkill.objects.filter(provider=profile, skill=self.skill).count(),
            1,
        )

    def test_marketplace_search_and_provider_detail(self):
        profile = ProviderProfile.objects.create(
            user=self.provider,
            full_name='Priya Sharma',
            location='Hingoli',
            experience=4,
            bio='Expert tailor',
        )
        ProviderSkill.objects.create(provider=profile, skill=self.skill)

        response = self.client.get(reverse('marketplace'), {
            'skill': 'Tailor',
            'location': 'Hingoli',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Priya Sharma')
        self.assertContains(response, reverse('provider_detail', args=[profile.id]))

        empty = self.client.get(reverse('marketplace'), {
            'skill': 'Baking',
            'location': 'Pune',
        })
        self.assertContains(empty, 'No providers found')

        detail = self.client.get(reverse('provider_detail', args=[profile.id]))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, 'Priya Sharma')
        self.assertContains(detail, '9991112222')

    def test_customer_dashboard_lists_providers(self):
        profile = ProviderProfile.objects.create(
            user=self.provider,
            full_name='Priya Sharma',
            location='Hingoli',
            experience=4,
        )
        self.client.login(username='customer1', password='StrongPass123!')
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Priya Sharma')
        self.assertContains(response, reverse('provider_detail', args=[profile.id]))

    def test_edit_profile_updates_fields(self):
        ProviderProfile.objects.create(
            user=self.provider,
            full_name='Priya Sharma',
            location='Hingoli',
            experience=4,
        )
        self.client.login(username='provider1', password='StrongPass123!')
        response = self.client.post(reverse('edit_profile'), {
            'full_name': 'Priya K',
            'bio': 'Updated bio',
            'location': 'Nanded',
            'experience': 6,
        })
        self.assertRedirects(response, reverse('my_profile'))
        profile = ProviderProfile.objects.get(user=self.provider)
        self.assertEqual(profile.full_name, 'Priya K')
        self.assertEqual(profile.location, 'Nanded')

    def test_portfolio_upload_requires_skill_and_saves(self):
        profile = ProviderProfile.objects.create(
            user=self.provider,
            full_name='Priya Sharma',
            location='Hingoli',
            experience=4,
        )
        self.client.login(username='provider1', password='StrongPass123!')
        blocked = self.client.get(reverse('add_portfolio'))
        self.assertRedirects(blocked, reverse('add_skill'))

        ProviderSkill.objects.create(provider=profile, skill=self.skill)
        image = make_test_image()
        response = self.client.post(reverse('add_portfolio'), {
            'skill': self.skill.id,
            'title': 'Blouse design',
            'description': 'Custom blouse',
            'image': image,
        })
        self.assertRedirects(response, reverse('my_profile'))
        self.assertEqual(Portfolio.objects.filter(provider=profile).count(), 1)
