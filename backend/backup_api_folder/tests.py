import os
from django.test import TestCase
from django.urls import reverse, resolve
from django.core.files import File

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from django.contrib.auth.models import User
from api.models import Administrador, Qualificacio, Interval, Metrica, ResultatEntrenament, ResultatInferencia, Entrenament, \
    Inferencia, Model
from . import permissions
from gaissalabel import settings


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


class TestEtiquetes(TestCase):

    def setUp(self) -> None:
        # Qualificacions
        self.qualificacioA = Qualificacio.objects.create(id='A', ordre=1)
        self.qualificacioB = Qualificacio.objects.create(id='B', ordre=2)
        self.qualificacioC = Qualificacio.objects.create(id='C', ordre=3)
        self.qualificacioD = Qualificacio.objects.create(id='D', ordre=4)
        self.qualificacioE = Qualificacio.objects.create(id='E', ordre=3)

        # Mètriques
        self.metricaE = Metrica.objects.create(id='metricaE', nom='Metrica entrenament', fase=Metrica.TRAIN, pes=0.5)
        self.metricaE2 = Metrica.objects.create(id='metricaE2', nom='Metrica entrenament 2', fase=Metrica.TRAIN, pes=0.5)
        self.metricaI = Metrica.objects.create(id='metricaI', nom='Metrica inferència', fase=Metrica.INF, pes=1)

        # Intervals
        with open('api/label_design/CO2_test.jpg', 'rb') as image_file:
            image = File(image_file)
            Interval.objects.create(id=1, metrica=self.metricaE, qualificacio=self.qualificacioA,
                                                  limitInferior=0, limitSuperior=100000000000, imatge=image)
            Interval.objects.create(id=2, metrica=self.metricaE, qualificacio=self.qualificacioB,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=3, metrica=self.metricaE, qualificacio=self.qualificacioC,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=4, metrica=self.metricaE, qualificacio=self.qualificacioD,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=5, metrica=self.metricaE, qualificacio=self.qualificacioE,
                                                  limitInferior=0, limitSuperior=0, imatge=image)

            Interval.objects.create(id=6, metrica=self.metricaE2, qualificacio=self.qualificacioA,
                                                  limitInferior=0, limitSuperior=100000000000, imatge=image)
            Interval.objects.create(id=7, metrica=self.metricaE2, qualificacio=self.qualificacioB,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=8, metrica=self.metricaE2, qualificacio=self.qualificacioC,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=9, metrica=self.metricaE2, qualificacio=self.qualificacioD,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=10, metrica=self.metricaE2, qualificacio=self.qualificacioE,
                                                  limitInferior=0, limitSuperior=0, imatge=image)

            Interval.objects.create(id=11, metrica=self.metricaI, qualificacio=self.qualificacioA,
                                                  limitInferior=0, limitSuperior=100000000000, imatge=image)
            Interval.objects.create(id=12, metrica=self.metricaI, qualificacio=self.qualificacioB,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=13, metrica=self.metricaI, qualificacio=self.qualificacioC,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=14, metrica=self.metricaI, qualificacio=self.qualificacioD,
                                                  limitInferior=0, limitSuperior=0, imatge=image)
            Interval.objects.create(id=15, metrica=self.metricaI, qualificacio=self.qualificacioE,
                                                  limitInferior=0, limitSuperior=0, imatge=image)

        # Model
        self.model = Model.objects.create(id=1, nom='Model prova')

        # Entrenament
        self.entrenament = Entrenament.objects.create(id=1, model=self.model)

        # Inferència
        self.inferencia = Inferencia.objects.create(id=1, model=self.model)

        # Resultats mètriques
        self.resultatME = ResultatEntrenament.objects.create(entrenament=self.entrenament, metrica=self.metricaE, valor=2)
        self.resultatME2 = ResultatEntrenament.objects.create(entrenament=self.entrenament, metrica=self.metricaE2, valor=None)
        self.resultatI = ResultatInferencia.objects.create(inferencia=self.inferencia, metrica=self.metricaI, valor=2)

    def tearDown(self) -> None:
        # Esborrem les imatges de prova dels intervals de la carpeta label_desgin
        folder_path = 'api/label_design'

        # Walk through the directory and delete images containing '_test_'
        for root, dirs, files in os.walk(os.path.join(settings.BASE_DIR, folder_path)):
            for file_name in files:
                if '_test_' in file_name:
                    file_path = os.path.join(root, file_name)
                    if os.path.exists(file_path):
                        os.remove(file_path)

    # Etiqueta entrenament
    def test_etiqueta_entrenament(self):
        # URL on farem la crida
        url = reverse('entrenaments-detail', kwargs={'model_id': 1, 'pk': 1})

        # Preparem i executem un GET
        request = APIRequestFactory().get(url)
        view = resolve(url).func
        response = view(request, model_id=1, pk=1)

        # Comprovem que hem pogut obtenir l'entrenament
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Etiqueta inferència
    def test_etiqueta_inferencia(self):
        # URL on farem la crida
        url = reverse('inferencies-detail', kwargs={'model_id': 1, 'pk': 1})

        # Preparem i executem un GET
        request = APIRequestFactory().get(url)
        view = resolve(url).func
        response = view(request, model_id=1, pk=1)

        # Comprovem que hem pogut obtenir la inferència
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Registrar entrenament
    def test_registrar_entrenament(self):
        # URL on farem la crida
        url = reverse('entrenaments-list', kwargs={'model_id': 1})

        data = {
            "resultats_info": {
                self.metricaE.id: 32,
                self.metricaE2.id: 2,
            },
            "infoAddicional_valors": {}
        }

        # Preparem i executem un POST
        request = APIRequestFactory().post(url, data=data, format='json')
        view = resolve(url).func
        response = view(request, model_id=1)

        # Comprovem que s'ha creat l'entrenament
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Registrar inferencia
    def test_registrar_inferencia(self):
        # URL on farem la crida
        url = reverse('inferencies-list', kwargs={'model_id': 1})

        data = {
            "resultats_info": {
                self.metricaI.id: 32,
            },
            "infoAddicional_valors": {}
        }

        # Preparem i executem un POST
        request = APIRequestFactory().post(url, data=data, format='json')
        view = resolve(url).func
        response = view(request, model_id=1)

        # Comprovem que s'ha creat l'entrenament
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


