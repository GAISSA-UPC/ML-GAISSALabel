from django.test import TestCase
from django.urls import reverse, resolve

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from django.contrib.auth.models import User
from .models import Administrador


class TestUsuari(APITestCase):
    def setUp(self):
        self.username = 'administrador'
        self.password = 'adminadmin'
        # Usuaris
        self.userAdmin = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.administrador = Administrador.objects.create(
            user=self.userAdmin,
        )

    def test_successful_register_and_login_admin(self):
        # URL on farem la crida
        url = reverse('login_admins-list')

        # Preparar i executar la request
        response = self.client.post(url, {'username': self.username, 'password': self.password}, format='json')

        # Assegurar-se que ha estat correcte
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
