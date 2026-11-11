from django.test import TestCase
from accounts.forms import RegistrationForm

class TestForms(TestCase):

    def test_registration_form_valid_data(self):
        """Test that the form is valid with correct data."""
        form = RegistrationForm(data={
            'first_name': 'first',
            'last_name': 'last',
            'phone_number': '11122233344',
            'email': 'user1@example.com',
            'username': 'first_last',
            'password': 'testpass123',
            'confirm_password': 'testpass123'  # Ensure this matches the password
        })

        if not form.is_valid():
            print(form.errors)  # Print the form errors for debugging

        self.assertTrue(form.is_valid())  # This should pass if everything is correct

    def test_registration_form_no_data(self):
        """Test that the form is invalid with no data."""
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_registration_form_invalid_password(self):
        """Test that the form is invalid if passwords don't match."""
        form = RegistrationForm(data={
            'first_name': 'first',
            'last_name': 'last',
            'phone_number': '11122233344',
            'email': 'user1@example.com',
            'username': 'first_last',
            'password': 'testpass123',
            'confirm_password': 'mismatchpassword'  # Password mismatch
        })
        
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('Password does not match!', form.errors['__all__'])
