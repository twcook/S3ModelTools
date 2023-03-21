from django.test import TestCase
from django.contrib.auth.models import User

# from component.views import AttestationList, AttestationCreate, AttestationUpdate 
from ..models import Project, Modeler, Attestation, Audit, XdBoolean, Cluster, XdCount, DM, XdFile, XdFloat, XdInterval, XdLink, \
    XdOrdinal, Participation, Party, XdQuantity, ReferenceRange, SimpleReferenceRange, XdString, XdTemporal, Units, Namespace, SemanticLink


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


class AuditTests(TestCase):


    def test_audit_list(self):
        response = self.client.get('/component/audit/')
        self.assertEqual(response.status_code, 200)

    def test_audit_create(self):
        response = self.client.get('/component/audit/create/')
        self.assertEqual(response.status_code, 200)

    def test_audit_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        audit = Audit.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/audit/update/' + str(audit.pk) + '/')
        self.assertEqual(response.status_code, 200)

class BooleanTests(TestCase):


    def test_boolean_list(self):
        response = self.client.get('/component/boolean/')
        self.assertEqual(response.status_code, 200)

    def test_boolean_create(self):
        response = self.client.get('/component/boolean/create/')
        self.assertEqual(response.status_code, 200)

    def test_boolean_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        boolean = XdBoolean.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/boolean/update/' + str(boolean.pk) + '/')
        self.assertEqual(response.status_code, 200)


class ClusterTests(TestCase):


    def test_cluster_list(self):
        response = self.client.get('/component/cluster/')
        self.assertEqual(response.status_code, 200)

    def test_cluster_create(self):
        response = self.client.get('/component/cluster/create/')
        self.assertEqual(response.status_code, 200)

    def test_cluster_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = Cluster.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/cluster/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class CountTests(TestCase):


    def test_count_list(self):
        response = self.client.get('/component/count/')
        self.assertEqual(response.status_code, 200)

    def test_count_create(self):
        response = self.client.get('/component/count/create/')
        self.assertEqual(response.status_code, 200)

    def test_count_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdCount.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/count/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class DataModelTests(TestCase):


    def test_datamodel_list(self):
        response = self.client.get('/component/datamodel/')
        self.assertEqual(response.status_code, 200)

    def test_datamodel_create(self):
        response = self.client.get('/component/datamodel/create/')
        self.assertEqual(response.status_code, 200)

    def test_datamodel_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = DM.objects.create(project=project, title='test', description='test', author=modeler, creator=modeler, edited_by=modeler)
        response = self.client.get('/component/datamodel/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class FileTests(TestCase):


    def test_file_list(self):
        response = self.client.get('/component/file/')
        self.assertEqual(response.status_code, 200)

    def test_file_create(self):
        response = self.client.get('/component/file/create/')
        self.assertEqual(response.status_code, 200)

    def test_file_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdFile.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/file/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class FloatTests(TestCase):


    def test_float_list(self):
        response = self.client.get('/component/float/')
        self.assertEqual(response.status_code, 200)

    def test_float_create(self):
        response = self.client.get('/component/float/create/')
        self.assertEqual(response.status_code, 200)

    def test_float_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdFloat.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/float/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class IntervalTests(TestCase):


    def test_interval_list(self):
        response = self.client.get('/component/interval/')
        self.assertEqual(response.status_code, 200)

    def test_interval_create(self):
        response = self.client.get('/component/interval/create/')
        self.assertEqual(response.status_code, 200)

    def test_interval_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdInterval.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/interval/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class LinkTests(TestCase):


    def test_link_list(self):
        response = self.client.get('/component/link/')
        self.assertEqual(response.status_code, 200)

    def test_link_create(self):
        response = self.client.get('/component/link/create/')
        self.assertEqual(response.status_code, 200)

    def test_link_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdLink.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/link/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class OrdinalTests(TestCase):


    def test_ordinal_list(self):
        response = self.client.get('/component/ordinal/')
        self.assertEqual(response.status_code, 200)

    def test_ordinal_create(self):
        response = self.client.get('/component/ordinal/create/')
        self.assertEqual(response.status_code, 200)

    def test_ordinal_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdOrdinal.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/ordinal/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class ParticipationTests(TestCase):


    def test_participation_list(self):
        response = self.client.get('/component/participation/')
        self.assertEqual(response.status_code, 200)

    def test_participation_create(self):
        response = self.client.get('/component/participation/create/')
        self.assertEqual(response.status_code, 200)

    def test_participation_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = Participation.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/participation/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class PartyTests(TestCase):


    def test_party_list(self):
        response = self.client.get('/component/party/')
        self.assertEqual(response.status_code, 200)

    def test_party_create(self):
        response = self.client.get('/component/party/create/')
        self.assertEqual(response.status_code, 200)

    def test_party_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = Party.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/party/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class QuantityTests(TestCase):


    def test_quantity_list(self):
        response = self.client.get('/component/quantity/')
        self.assertEqual(response.status_code, 200)

    def test_quantity_create(self):
        response = self.client.get('/component/quantity/create/')
        self.assertEqual(response.status_code, 200)

    def test_quantity_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdQuantity.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/quantity/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class ReferenceRangeTests(TestCase):


    def test_referencerange_list(self):
        response = self.client.get('/component/referencerange/')
        self.assertEqual(response.status_code, 200)

    def test_referencerange_create(self):
        response = self.client.get('/component/referencerange/create/')
        self.assertEqual(response.status_code, 200)

    def test_referencerange_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        invl = XdInterval.objects.create(project=project, label='test', description='test')
        comp = ReferenceRange.objects.create(project=project, interval=invl, label='test', description='test')
        response = self.client.get('/component/referencerange/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class SimpleReferenceRangeTests(TestCase):


    def test_simplereferencerange_list(self):
        response = self.client.get('/component/simplereferencerange/')
        self.assertEqual(response.status_code, 200)

    def test_simplereferencerange_create(self):
        response = self.client.get('/component/simplereferencerange/create/')
        self.assertEqual(response.status_code, 200)

    def test_simplereferencerange_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = SimpleReferenceRange.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/simplereferencerange/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class StringTests(TestCase):


    def test_string_list(self):
        response = self.client.get('/component/string/')
        self.assertEqual(response.status_code, 200)

    def test_string_create(self):
        response = self.client.get('/component/string/create/')
        self.assertEqual(response.status_code, 200)

    def test_string_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdString.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/string/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class TemporalTests(TestCase):


    def test_temporal_list(self):
        response = self.client.get('/component/temporal/')
        self.assertEqual(response.status_code, 200)

    def test_temporal_create(self):
        response = self.client.get('/component/temporal/create/')
        self.assertEqual(response.status_code, 200)

    def test_temporal_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = XdTemporal.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/temporal/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


class UnitsTests(TestCase):


    def test_units_list(self):
        response = self.client.get('/component/units/')
        self.assertEqual(response.status_code, 200)

    def test_units_create(self):
        response = self.client.get('/component/units/create/')
        self.assertEqual(response.status_code, 200)

    def test_units_update(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="Test User", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name")
        comp = Units.objects.create(project=project, label='test', description='test')
        response = self.client.get('/component/units/update/' + str(comp.pk) + '/')
        self.assertEqual(response.status_code, 200)


