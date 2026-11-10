from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import UserRegistrationForm

User = get_user_model()


class RoleSyncTests(TestCase):
    def test_registration_syncs_profile_role_to_django_permissions(self):
        form = UserRegistrationForm(data={
            'username': 'adminuser',
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'role': 'admin',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertEqual(user.profile.role, 'admin')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_profile_update_syncs_role_to_user_permissions(self):
        user = User.objects.create_user(username='staffuser', email='staff@example.com', password='StrongPass123!')
        user.profile.role = 'staff'
        user.profile.save()
        user.is_staff = False
        user.is_superuser = False
        user.save()

        self.client.force_login(user)
        response = self.client.post(
            reverse('accounts:profile'),
            {
                'phone': '08012345678',
                'address': 'Lagos',
                'role': 'admin',
                'first_name': 'Staff',
                'last_name': 'Profile',
                'email': 'staff@example.com',
            },
        )

        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.profile.role, 'admin')

    def test_anonymous_user_can_create_account(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('accounts:register'),
            {
                'username': 'newmember',
                'first_name': 'New',
                'last_name': 'Member',
                'email': 'newmember@example.com',
                'role': 'staff',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newmember').exists())
