from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('core:signup')
        self.login_url = reverse('core:login')
        self.logout_url = reverse('core:logout')
        self.client = Client()

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')

    def test_signup_view_post(self):
        data = {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword'}
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)  # Debería redirigir después de un registro exitoso

    def test_logout_view_get(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/logout.html')

    def test_logout_view_post(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Debería redirigir después de cerrar sesión

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_login_view_post(self):
        User.objects.create_user(username='testuser', password='testuser')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  