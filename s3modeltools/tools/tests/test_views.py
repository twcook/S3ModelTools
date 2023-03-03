from django.test import TestCase


class ToolsTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_aboutpage(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

