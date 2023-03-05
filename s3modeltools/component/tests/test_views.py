from django.test import TestCase

# from component.views import AttestationList, AttestationCreate, AttestationUpdate 

class AttestationTests(TestCase):

    def test_attestation_list(self):
        response = self.client.get('/component/attestation/')
        self.assertEqual(response.status_code, 200)

    def test_attestation_create(self):
        response = self.client.get('/component/attestation/create/')
        self.assertEqual(response.status_code, 200)

    def test_attestation_update(self):
        response = self.client.get('/component/attestation/update/1')
        self.assertEqual(response.status_code, 200)
