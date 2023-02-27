from django.test import TestCase
from django.contrib.auth.models import User

from tools.models import Project, Modeler
from ..models import NS, Predicate, PredObj, XdBoolean, XdLink, XdString, Units, \
                     XdFile

class PredObjModelTest(TestCase):

    def test_ns_string_representation(self):
        ns = NS(abbrev = "S3M", uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd")
        self.assertEqual(str(ns), ns.abbrev.strip())

    def test_ns_uri_too_long(self):
        ns = NS(abbrev = "S3M", uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI#SomeVeryVeryLong URI")
        self.assertGreater(len( ns.uri.strip()), 1024)

    def test_predicate_string_representation(self):
        ns = NS(abbrev = "S3M", uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd")
        predicate = Predicate(ns_abbrev = ns, class_name="A Class") 
        self.assertEqual(str(predicate), ns.abbrev + ":" + predicate.class_name.strip())    

    def test_predobj_string_representation(self):
        project = Project(prj_name="My Project Name")
        ns = NS(abbrev = "S3M", uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd")
        predicate = Predicate(ns_abbrev = ns, class_name="A Class") 
        predobj = PredObj(po_name="PredObj Name", predicate = predicate, project=project)
        self.assertEqual(str(predobj), predobj.project.prj_name + ' { ' + predobj.po_name.strip() + ' } ' + predobj.predicate.__str__() + " --> " + predobj.object_uri.strip())

class XdBooleanModelTest(TestCase):

    def test_xdboolean_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdboolean = XdBoolean.objects.create(label="XdBoolean Name", project=project, creator=modeler, trues="True", falses="False")
        self.assertEqual(str(xdboolean), xdboolean.project.prj_name + ' : ' + xdboolean.label)

    def test_xdboolean_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdboolean = XdBoolean.objects.create(label="XdBoolean Name", project=project, creator=modeler, trues="True", falses="False")
        self.assertEqual(xdboolean.public, True)
        self.assertNotEqual(xdboolean.ct_id, "")
        self.assertNotEqual(xdboolean.created, None)
        self.assertEqual(xdboolean.published, False)
        self.assertNotEqual(xdboolean.adapter_ctid, "")
        self.assertEqual(xdboolean.ui_type, 'Choose UI Type:')
        self.assertEqual(xdboolean.trues, "True")
        self.assertEqual(xdboolean.falses, "False")

class XdLinkModelTest(TestCase):
    
        def test_xdlink_string_representation(self):
            project = Project.objects.create(prj_name="My Project Name")
            user=User.objects.create(username="TestUser", password="passw0rd")
            modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
            xdlink = XdLink.objects.create(label="XdLink Name", project=project, creator=modeler)
            self.assertEqual(str(xdlink), xdlink.project.prj_name + ' : ' + xdlink.label)
    
        def test_xdlink_default_values(self):
            project = Project.objects.create(prj_name="My Project Name")
            user=User.objects.create(username="TestUser", password="passw0rd")
            modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
            xdlink = XdLink.objects.create(label="XdLink Name", project=project, creator=modeler, \
                                           link="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd", \
                                            relation="part of", \
                                                relation_uri="http://purl.obolibrary.org/obo/BFO_0000050")
            self.assertNotEqual(xdlink.ct_id, "")
            self.assertNotEqual(xdlink.created, None)
            self.assertEqual(xdlink.published, False)
            self.assertNotEqual(xdlink.adapter_ctid, "")
            self.assertEqual(xdlink.relation, "part of")
            self.assertEqual(xdlink.ui_type, 'Choose UI Type:')

class XdStringModelTest(TestCase):
    
    def test_xdstring_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdstring = XdString.objects.create(label="XdString Name", project=project, creator=modeler)
        self.assertEqual(str(xdstring), xdstring.project.prj_name + ' : ' + xdstring.label)

    def test_xdstring_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdstring = XdString.objects.create(label="XdString Name", project=project, creator=modeler, \
                                            max_length=25, min_length=3, str_fmt="^[a-zA-Z0-9_]*$")
        self.assertNotEqual(xdstring.ct_id, "")
        self.assertNotEqual(xdstring.created, None)
        self.assertEqual(xdstring.published, False)
        self.assertNotEqual(xdstring.adapter_ctid, "")
        self.assertEqual(xdstring.ui_type, 'Choose UI Type:')
        self.assertEqual(xdstring.max_length, 25)
        self.assertEqual(xdstring.min_length, 3)
        self.assertEqual(xdstring.str_fmt, "^[a-zA-Z0-9_]*$")

class UnitsModelTest(TestCase):

    def test_units_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        units = Units.objects.create(label="Units Name", project=project, creator=modeler)
        self.assertEqual(str(units), units.project.prj_name + ' : ' + units.label)

    def test_units_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        units = Units.objects.create(label="Units Name", project=project, creator=modeler, \
                                    enums="m\ncm", \
                                    definitions="http://www.ontology-of-units-of-measure.org/resource/om-2/meter\n" \
                                        "http://www.ontology-of-units-of-measure.org/resource/om-2/centimeter")                
        self.assertNotEqual(units.ct_id, "")
        self.assertNotEqual(units.created, None)
        self.assertEqual(units.published, False)
        self.assertNotEqual(units.adapter_ctid, "")
        self.assertEqual(units.ui_type, 'Choose UI Type:')
        self.assertEqual(units.enums, "m\ncm")
        self.assertEqual(units.definitions, "http://www.ontology-of-units-of-measure.org/resource/om-2/meter\nhttp://www.ontology-of-units-of-measure.org/resource/om-2/centimeter")

class XdFileModelTest(TestCase):
    
    def test_xdfile_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdfile = XdFile.objects.create(label="XdFile Name", project=project, creator=modeler)
        self.assertEqual(str(xdfile), xdfile.project.prj_name + ' : ' + xdfile.label)

    def test_xdfile_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdfile = XdFile.objects.create(label="XdFile Name", project=project, creator=modeler, \
                                        media_type="text/html\njson")

        self.assertEqual(xdfile.label, "XdFile Name")
        self.assertNotEqual(xdfile.ct_id, "")
        self.assertNotEqual(xdfile.created, None)
        self.assertEqual(xdfile.published, False)
        self.assertNotEqual(xdfile.adapter_ctid, "")
        self.assertEqual(xdfile.content_mode, 'Select Mode:')
        self.assertEqual(xdfile.alt_txt, '')
        self.assertEqual(xdfile.encoding, 'utf-8')
        self.assertEqual(xdfile.language, "en-US")
