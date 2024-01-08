from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from django.contrib.auth.models import User
from .models import Administrador
from . import permissions


class TestUsuari(APITestCase):
    def setUp(self):
        self.username = 'administrador'
        self.password = 'adminadmin'
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


class TestPermissions(TestCase):

    def setUp(self) -> None:
        # Admin
        self.userAdmin = User.objects.create(
            id=1,
            username='usuariAdmin',
            is_active=True
        )
        self.admin = Administrador.objects.create(
            user=self.userAdmin
        )

    # IsAuthenticated
    def test_authenticated_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userAdmin
        permission = permissions.IsAuthenticated()
        self.assertTrue(permission.has_permission(request))

    # Si no hi ha usuari no està autenticat
    def test_authenticated_false(self):
        request = APIRequestFactory().get('')
        request.user = None
        permission = permissions.IsAuthenticated()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si ets administrador
    def test_admin_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userAdmin
        permission = permissions.IsAdmin()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si no ets administrador
    def test_admin_false(self):
        request = APIRequestFactory().get('')
        request.user = None
        permission = permissions.IsAdmin()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si no estàs autenticat pots GET en IsAdminEditOthersRead
    def test_othersread_true(self):
        request = APIRequestFactory().get('')
        request.user = None
        permission = permissions.IsAdminEditOthersRead()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si no ets admin no pots POST en IsAdminEditOthersRead
    def test_otherswrite_false(self):
        request = APIRequestFactory().post('')
        request.user = None
        permission = permissions.IsAdminEditOthersRead()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si ets admin pots GET en IsAdminEditOthersRead
    def test_adminread_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userAdmin
        permission = permissions.IsAdminEditOthersRead()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si ets admin pots POST en IsAdminEditOthersRead
    def test_adminwrite_true(self):
        request = APIRequestFactory().post('')
        request.user = self.userAdmin
        permission = permissions.IsAdminEditOthersRead()
        self.assertTrue(permission.has_permission(request))

