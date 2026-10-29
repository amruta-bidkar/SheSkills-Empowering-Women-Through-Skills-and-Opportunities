from django.test import TestCase
from django.urls import reverse
from .models import User


class AccountsWorkflowTests(TestCase):
    def test_register_provider_and_reach_dashboard(self):
        response = self.client.post(reverse('register'), {
            'username': 'priya',
            'email': 'priya@example.com',
            'phone': '9876543210',
            'role': User.PROVIDER,
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('provider_dashboard'))
        self.assertTrue(User.objects.filter(username='priya', role='provider').exists())

    def test_register_customer_and_reach_dashboard(self):
        response = self.client.post(reverse('register'), {
            'username': 'anita',
            'email': 'anita@example.com',
            'phone': '9876543211',
            'role': User.CUSTOMER,
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('customer_dashboard'))

    def test_login_required_redirects_to_named_login(self):
        response = self.client.get(reverse('provider_dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('provider_dashboard')}"
        )

    def test_customer_cannot_open_provider_dashboard(self):
        User.objects.create_user(
            username='cust',
            password='StrongPass123!',
            role=User.CUSTOMER,
        )
        self.client.login(username='cust', password='StrongPass123!')
        response = self.client.get(reverse('provider_dashboard'))
        self.assertRedirects(response, reverse('customer_dashboard'))

    def test_logout_ends_session(self):
        User.objects.create_user(
            username='cust',
            password='StrongPass123!',
            role=User.CUSTOMER,
        )
        self.client.login(username='cust', password='StrongPass123!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_login_shows_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'missing',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')
