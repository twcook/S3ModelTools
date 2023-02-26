from django.test import TestCase
from django.contrib.auth.models import User

from tools.models import Project
from ..models import NS, Predicate, PredObj, XdBoolean, XdLink

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
        project = Project(prj_name="My Project Name")
        
        xdboolean = XdBoolean(label="XdBoolean Name", project=project)
        self.assertEqual(str(xdboolean), xdboolean.project.prj_name + ' : ' + xdboolean.label)