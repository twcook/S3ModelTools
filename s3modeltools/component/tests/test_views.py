from django.test import TestCase
from django.contrib.auth.models import User

# from component.views import AttestationList, AttestationCreate, AttestationUpdate 
from ..models import Project, Attestation, Modeler


class AttestationTests(TestCase):


    def test_attestation_list(self):
        response = self.client.get('/component/attestation/')
        self.assertEqual(response.status_code, 200)

    def test_attestation_create(self):
        response = self.client.get('/component/attestation/create/')
        self.assertEqual(response.status_code, 200)

    def test_attestation_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        atn = Attestation.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/attestation/update/' + str(atn.pk) + '/')
        self.assertEqual(response.status_code, 200)
