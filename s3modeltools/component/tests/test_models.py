import ast

from django.test import TestCase
from django.contrib.auth.models import User

from tools.models import Project, Modeler
from ..models import NS, Predicate, PredObj, XdBoolean, XdLink, XdString, Units, XdFile, XdInterval, ReferenceRange, \
    SimpleReferenceRange, XdOrdinal, XdTemporal, XdCount, XdQuantity, XdFloat, Party, Participation, Audit, Attestation, Cluster, DM

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

class XdIntervalModelTest(TestCase):
    
    def test_xdinterval_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdinterval = XdInterval.objects.create(label="XdInterval Name", project=project, creator=modeler)
        self.assertEqual(str(xdinterval), xdinterval.project.prj_name + ' : ' + xdinterval.label)

    def test_xdinterval_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdinterval = XdInterval.objects.create(label="XdInterval Name", project=project, creator=modeler, \
                                            lower='25', upper='100')
        self.assertNotEqual(xdinterval.ct_id, "")
        self.assertNotEqual(xdinterval.created, None)
        self.assertEqual(xdinterval.published, False)
        self.assertNotEqual(xdinterval.adapter_ctid, "")
        self.assertEqual(xdinterval.lower, '25')
        self.assertEqual(xdinterval.upper, '100')
        self.assertEqual(xdinterval.lower_bounded, True)
        self.assertEqual(xdinterval.lower_included, True)
        self.assertEqual(xdinterval.upper_bounded, True)
        self.assertEqual(xdinterval.upper_included, True)
        self.assertEqual(xdinterval.units_uri, None)
        self.assertEqual(xdinterval.units_name, None)

class ReferenceRangeModelTest(TestCase):

    def test_referencerange_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdinterval = XdInterval.objects.create(label="XdInterval Name", project=project, creator=modeler, \
                                            lower='25', upper='100')
        referencerange = ReferenceRange.objects.create(label="ReferenceRange Name", project=project, creator=modeler, \
                                                    definition='A Reference Range', interval=xdinterval)
        self.assertEqual(str(referencerange), referencerange.project.prj_name + ' : ' + referencerange.label)

    def test_referencerange_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdinterval = XdInterval.objects.create(label="XdInterval Name", project=project, creator=modeler, \
                                            lower='25', upper='100')
        referencerange = ReferenceRange.objects.create(label="ReferenceRange Name", project=project, creator=modeler, \
                                                    definition='A Reference Range', interval=xdinterval)
        self.assertNotEqual(referencerange.ct_id, "")
        self.assertNotEqual(referencerange.created, None)
        self.assertEqual(referencerange.published, False)
        self.assertNotEqual(referencerange.adapter_ctid, "")
        self.assertEqual(referencerange.definition, 'A Reference Range')
        self.assertEqual(referencerange.interval, xdinterval)
        self.assertEqual(referencerange.is_normal, False)

class SimpleReferenceRangeModelTest(TestCase):
    
    def test_srr_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        srr = SimpleReferenceRange.objects.create(label="srr Name", project=project, creator=modeler)
        self.assertEqual(str(srr), srr.project.prj_name + ' : ' + srr.label)

    def test_srr_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        srr = SimpleReferenceRange.objects.create(label="srr Name", project=project, creator=modeler, lower='25', upper='100', interval_type='int')
        self.assertNotEqual(srr.ct_id, "")
        self.assertNotEqual(srr.created, None)
        self.assertEqual(srr.published, False)
        self.assertNotEqual(srr.adapter_ctid, "")
        if srr.lower is not None and srr.upper is not None:
            self.assertEqual(type(ast.literal_eval(srr.lower)), type(ast.literal_eval(srr.upper)))


class XdOrdinalModelTests(TestCase):
        
    def test_xdordinal_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdordinal = XdOrdinal.objects.create(label="XdOrdinal Name", project=project, creator=modeler)
        self.assertEqual(str(xdordinal), xdordinal.project.prj_name + ' : ' + xdordinal.label)

    def test_xdordinal_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdordinal = XdOrdinal.objects.create(label="XdOrdinal Name", project=project, creator=modeler)
        self.assertNotEqual(xdordinal.ct_id, "")
        self.assertNotEqual(xdordinal.created, None)
        self.assertEqual(xdordinal.published, False)
        self.assertNotEqual(xdordinal.adapter_ctid, "")
        self.assertEqual(xdordinal.ordinals, '')
        self.assertEqual(xdordinal.symbols, '')
        self.assertEqual(xdordinal.annotations, '')

class XdTemporalModelTests(TestCase):
            
    def test_xdtemporal_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdtemporal = XdTemporal.objects.create(label="XdTemporal Name", project=project, creator=modeler)
        self.assertEqual(str(xdtemporal), xdtemporal.project.prj_name + ' : ' + xdtemporal.label)

    def test_xdtemporal_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdtemporal = XdTemporal.objects.create(label="XdTemporal Name", project=project, creator=modeler)
        self.assertNotEqual(xdtemporal.ct_id, "")
        self.assertNotEqual(xdtemporal.created, None)
        self.assertEqual(xdtemporal.published, False)
        self.assertNotEqual(xdtemporal.adapter_ctid, "")
        self.assertEqual(xdtemporal.allow_duration, False)
        self.assertEqual(xdtemporal.allow_date, False)
        self.assertEqual(xdtemporal.allow_time, False)
        self.assertEqual(xdtemporal.allow_datetime, False)
        self.assertEqual(xdtemporal.allow_day, False)
        self.assertEqual(xdtemporal.allow_month, False)
        self.assertEqual(xdtemporal.allow_month_day, False)
        self.assertEqual(xdtemporal.allow_year, False)
        self.assertEqual(xdtemporal.allow_year_month, False)

class XdCountModelTests(TestCase):
                    
    def test_xdcount_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdcount = XdCount.objects.create(label="XdCount Name", project=project, creator=modeler)
        self.assertEqual(str(xdcount), xdcount.project.prj_name + ' : ' + xdcount.label)

    def test_xdcount_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdcount = XdCount.objects.create(label="XdCount Name", project=project, creator=modeler)
        self.assertNotEqual(xdcount.ct_id, "")
        self.assertNotEqual(xdcount.created, None)
        self.assertEqual(xdcount.published, False)
        self.assertNotEqual(xdcount.adapter_ctid, "")
        self.assertEqual(xdcount.min_magnitude, None)
        self.assertEqual(xdcount.max_magnitude, None)
        self.assertEqual(xdcount.min_inclusive, None)
        self.assertEqual(xdcount.max_inclusive, None)
        self.assertEqual(xdcount.min_exclusive, None)
        self.assertEqual(xdcount.max_exclusive, None)
        self.assertEqual(xdcount.total_digits, None)
        self.assertEqual(xdcount.require_ms, False)
        self.assertEqual(xdcount.require_error, False)
        self.assertEqual(xdcount.require_accuracy, False)
        self.assertEqual(xdcount.allow_ms, False)
        self.assertEqual(xdcount.allow_error, False)
        self.assertEqual(xdcount.allow_accuracy, False)
        self.assertEqual(xdcount.units, None)

class XdQuantityModelTests(TestCase):
                            
    def test_xdquantity_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdquantity = XdQuantity.objects.create(label="XdQuantity Name", project=project, creator=modeler)
        self.assertEqual(str(xdquantity), xdquantity.project.prj_name + ' : ' + xdquantity.label)

    def test_xdquantity_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdquantity = XdQuantity.objects.create(label="XdQuantity Name", project=project, creator=modeler)
        self.assertNotEqual(xdquantity.ct_id, "")
        self.assertNotEqual(xdquantity.created, None)
        self.assertEqual(xdquantity.published, False)
        self.assertNotEqual(xdquantity.adapter_ctid, "")
        self.assertEqual(xdquantity.min_magnitude, None)
        self.assertEqual(xdquantity.max_magnitude, None)
        self.assertEqual(xdquantity.min_inclusive, None)
        self.assertEqual(xdquantity.max_inclusive, None)
        self.assertEqual(xdquantity.min_exclusive, None)
        self.assertEqual(xdquantity.max_exclusive, None)
        self.assertEqual(xdquantity.total_digits, None)
        self.assertEqual(xdquantity.require_ms, False)
        self.assertEqual(xdquantity.require_error, False)
        self.assertEqual(xdquantity.require_accuracy, False)
        self.assertEqual(xdquantity.allow_ms, False)
        self.assertEqual(xdquantity.allow_error, False)
        self.assertEqual(xdquantity.allow_accuracy, False)
        self.assertEqual(xdquantity.units, None)

class XdFloatModelTests(TestCase):
                                    
    def test_xdfloat_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdfloat = XdFloat.objects.create(label="XdFloat Name", project=project, creator=modeler)
        self.assertEqual(str(xdfloat), xdfloat.project.prj_name + ' : ' + xdfloat.label)

    def test_xdfloat_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdfloat = XdFloat.objects.create(label="XdFloat Name", project=project, creator=modeler)
        self.assertNotEqual(xdfloat.ct_id, "")
        self.assertNotEqual(xdfloat.created, None)
        self.assertEqual(xdfloat.published, False)
        self.assertNotEqual(xdfloat.adapter_ctid, "")
        self.assertEqual(xdfloat.min_magnitude, None)
        self.assertEqual(xdfloat.max_magnitude, None)
        self.assertEqual(xdfloat.min_inclusive, None)
        self.assertEqual(xdfloat.max_inclusive, None)
        self.assertEqual(xdfloat.min_exclusive, None)
        self.assertEqual(xdfloat.max_exclusive, None)
        self.assertEqual(xdfloat.total_digits, None)
        self.assertEqual(xdfloat.require_ms, False)
        self.assertEqual(xdfloat.require_error, False)
        self.assertEqual(xdfloat.require_accuracy, False)
        self.assertEqual(xdfloat.allow_ms, False)
        self.assertEqual(xdfloat.allow_error, False)
        self.assertEqual(xdfloat.allow_accuracy, False)
        self.assertEqual(xdfloat.units, None)   

class PartyModelTests(TestCase):

    def test_party_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        self.assertEqual(str(party), party.project.prj_name + ' : ' + party.label)

    def test_party_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        self.assertNotEqual(party.ct_id, "")
        self.assertNotEqual(party.created, None)
        self.assertEqual(party.published, False)
        self.assertNotEqual(party.adapter_ctid, "")
        self.assertEqual(party.details, None)
        self.assertEqual(party.external_ref, None)
