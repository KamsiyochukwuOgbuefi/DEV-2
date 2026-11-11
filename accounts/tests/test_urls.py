from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import (
    register, login, logout, client_dashboard, activate, forgotPassword, resetpassword_validate, resetPassword,
    admin_register, admin_login, admin_logout, admin_activate, admin_forgot_password,
    admin_resetpassword_validate, admin_reset_password
)

from accounts.models import Account

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def validate_url(name, uidb64, token):
    return reverse(name, args=[uidb64, token])

class TestUrls(TestCase):

    def setUp(self):
        self.user1 = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )

    def test_register_urls_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_urls_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login)

    def test_logout_urls_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout)

    def test_client_dashboard_urls_resolves(self):
        url = reverse('client_dashboard')
        self.assertEqual(resolve(url).func, client_dashboard)

    def test_activate_urls_resolves(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = validate_url('activate', uidb64, token)
        self.assertEqual(resolve(url).func, activate)

    def test_forgotPassword_urls_resolves(self):
        url = reverse('forgotPassword')
        self.assertEqual(resolve(url).func, forgotPassword)

    def test_resetpassword_validate_urls_resolves(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = validate_url('resetpassword_validate', uidb64, token)
        self.assertEqual(resolve(url).func, resetpassword_validate)

    def test_resetPassword_urls_resolves(self):
        url = reverse('resetPassword')
        self.assertEqual(resolve(url).func, resetPassword)

    def test_admin_register_urls_resolves(self):
        url = reverse('admin_register')
        self.assertEqual(resolve(url).func, admin_register)

    def test_admin_login_urls_resolves(self):
        url = reverse('admin_login')
        self.assertEqual(resolve(url).func, admin_login)

    def test_admin_logout_urls_resolves(self):
        url = reverse('admin_logout')
        self.assertEqual(resolve(url).func, admin_logout)

    def test_admin_activate_urls_resolves(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = validate_url('admin_activate', uidb64, token)
        self.assertEqual(resolve(url).func, admin_activate)

    def test_admin_forgot_password_urls_resolves(self):
        url = reverse('admin_forgot_password')
        self.assertEqual(resolve(url).func, admin_forgot_password)

    def test_admin_resetpassword_validate_urls_resolves(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = validate_url('admin_resetpassword_validate', uidb64, token)
        self.assertEqual(resolve(url).func, admin_resetpassword_validate)

    def test_admin_resetpassword_urls_resolves(self):
        url = reverse('admin_reset_password')
        self.assertEqual(resolve(url).func, admin_reset_password)