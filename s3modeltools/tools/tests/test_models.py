from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Project, Modeler


class ProjectModelTest(TestCase):

    def test_string_representation(self):
        project = Project(prj_name="My Project Name")
        project.description = "My Project Description" 
        self.assertEqual(str(project), project.prj_name)
        self.assertEqual(project.description, "My Project Description")

class ModelerModelTest(TestCase):
    
    def test_string_representation(self):
        project = Project(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler(user=user, name="Test Modeler Name", project=project)
        self.assertEqual(str(modeler), modeler.name.strip())

    def test_modeler_user(self):
        project = Project(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler(user=user, name="Test Modeler Name", project=project)
        self.assertEqual(modeler.user.username, "TestUser")

    def test_modeler_project(self):
        project = Project(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler(user=user, name="Test Modeler Name", project=project)
        self.assertEqual(modeler.project.prj_name, "My Project Name")
        