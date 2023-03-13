import ast

from django.test import TestCase
from django.contrib.auth.models import User

from tools.models import Project, Modeler
from ..models import Predicate, PredObj, XdBoolean, XdLink, XdString, Units, XdFile, XdInterval, ReferenceRange, \
    SimpleReferenceRange, XdOrdinal, XdTemporal, XdCount, XdQuantity, XdFloat, Party, Participation, Audit, Attestation, Cluster, DM


# class PredObjModelTest(TestCase):
#     """
#     Test PredObj model
#     TODO: Add tests for all elements.
#     """

#     def test_predobj_string_representation(self):
#         project = Project(prj_name="My Project Name")
#         pred = Predicate.objects.create(ns_abbrev = "S3M", class_name="isPartOf", ns_uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd")
#         predoj = PredObj.objects.create(po_name="PredObj Name", predicate = pred, project=project, object_uri="https://www.s3model.com/ns/s3m#isPartOf")
#         self.assertEqual(str(predoj), pred.ns_abbrev.strip() + ":" + pred.class_name.strip())

#     def test_predicate_string_representation(self):
#         predicate = Predicate.objects.create(ns_abbrev = "s3m", class_name="isPartOf", ns_uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd") 
#         self.assertEqual(str(predicate), .abbrev + ":" + predicate.class_name.strip())    

#     def test_predobj_string_representation(self):
#         project = Project(prj_name="My Project Name")
#         ns = NS(abbrev = "S3M", uri = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd")
#         predicate = Predicate(ns_abbrev = ns, class_name="A Class") 
#         predobj = PredObj(po_name="PredObj Name", predicate = predicate, project=project)
#         self.assertEqual(str(predobj), predobj.project.prj_name + ' { ' + predobj.po_name.strip() + ' } ' + predobj.predicate.__str__() + " --> " + predobj.object_uri.strip())


class XdBooleanModelTest(TestCase):
    """
    Test XdBoolean model
    TODO: Add tests for all elements.
    """

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
    """
    Test XdLink model
    TODO: Add tests for all elements.
    """    

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
    """
    Test module for XdString model
    TODO: Add tests for all elements.
    """    

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
    """
    Test Units model
    TODO: Add tests for all elements.
    """

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
    """
    Test module for XdFile model
    TODO: Add tests for all elements.
    """    

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
    """
    Test case for the XdInterval model
    TODO: Add tests for all elements.
    """    

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
    """
    Test module for ReferenceRange model
    TODO: Add tests for all elements.
    """

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
    """
    Test SimpleReferenceRange model
    TODO: Add tests for all elements.
    """

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
    """
    Test the XdOrdinal model
    TODO: Add tests for all elements.
    """    

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
    """
    Test the XdTemporal model
    TODO: Add tests for all elements.
    """            

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
    """
    Tests for the XdCount model
    TODO: Add tests for all elements.
    """                    

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
    """
    Test the XdQuantity model
    TODO: Add tests for all elements.
    """                            

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
    """
    Test the XdFloat model
    TODO: Test the XdFloat model elements
    """                                  

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
    """
    Test Party model
    TODO: Add tests for Party model elements
    """

    def test_party_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdlink = XdLink.objects.create(label="XdLink Name", project=project, creator=modeler)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler, details=None)
        self.assertEqual(str(party), party.project.prj_name + ' : ' + party.label)

    def test_party_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        xdlink = XdLink.objects.create(label="XdLink Name", project=project, creator=modeler)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler, details=None)
        self.assertNotEqual(party.ct_id, "")
        self.assertNotEqual(party.created, None)
        self.assertEqual(party.published, False)
        self.assertEqual(party.details, None)


class ParticipationModelTests(TestCase):
    """
    Tests for the Participation model
    TODO: Add tests for all elements of the Participation model
    """

    def test_participation_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        participation = Participation.objects.create(label="Participation Name", project=project, creator=modeler)
        self.assertEqual(str(participation), participation.project.prj_name + ' : ' + participation.label)

    def test_participation_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        participation = Participation.objects.create(label="Participation Name", project=project, creator=modeler)
        self.assertNotEqual(participation.ct_id, "")
        self.assertNotEqual(participation.created, None)
        self.assertEqual(participation.published, False)
        self.assertEqual(participation.performer, None)
        self.assertEqual(participation.function, None)
        self.assertEqual(participation.mode, None)


class AuditModelTests(TestCase):
    """
    Test Audit model
    TODO: Add tests for all values
    """

    def test_audit_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        audit = Audit.objects.create(label="Audit Name", project=project, creator=modeler)
        self.assertEqual(str(audit), audit.project.prj_name + ' : ' + audit.label)

    def test_audit_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        audit = Audit.objects.create(label="Audit Name", project=project, creator=modeler)
        self.assertNotEqual(audit.ct_id, "")
        self.assertNotEqual(audit.created, None)
        self.assertEqual(audit.published, False)
        self.assertEqual(audit.system_id, None)
        self.assertEqual(audit.system_user, None)
        self.assertEqual(audit.location, None)


class AttestationModelTests(TestCase):
    """ 
    Test the Attestation model
    TODO: Add tests for the elements of the Attestation model.
    """

    def test_attestation_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        attestation = Attestation.objects.create(label="Attestation Name", project=project, creator=modeler)
        self.assertEqual(str(attestation), attestation.project.prj_name + ' : ' + attestation.label)

    def test_attestation_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        party = Party.objects.create(label="Party Name", project=project, creator=modeler)
        attestation = Attestation.objects.create(label="Attestation Name", project=project, creator=modeler)
        self.assertNotEqual(attestation.ct_id, "")
        self.assertNotEqual(attestation.created, None)
        self.assertEqual(attestation.published, False)
        self.assertEqual(attestation.view, None)
        self.assertEqual(attestation.proof, None)
        self.assertEqual(attestation.reason, None)
        self.assertEqual(attestation.committer, None)


class ClusterModelTests(TestCase):
    """
    Test the Cluster model
    TODO: Test all of the models for single and multiple values.
    """

    def test_cluster_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        cluster = Cluster.objects.create(label="Cluster Name", project=project, creator=modeler)
        self.assertEqual(str(cluster), cluster.project.prj_name + ' : ' + cluster.label)

    def test_cluster_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        cluster = Cluster.objects.create(label="Cluster Name", project=project, creator=modeler)
        self.assertNotEqual(cluster.ct_id, "")
        self.assertNotEqual(cluster.created, None)
        self.assertEqual(cluster.published, False)


class DMModelTests(TestCase):
    """
    Test DM model.
    TODO: Add tests for metadata and other fields.
    """

    def test_dm_string_representation(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        dm = DM.objects.create(title="DM Name", project=project, creator=modeler, author=modeler, edited_by=modeler)
        self.assertEqual(str(dm), dm.project.prj_name + ' : ' + dm.title)

    def test_dm_default_values(self):
        project = Project.objects.create(prj_name="My Project Name")
        user=User.objects.create(username="TestUser", password="passw0rd")
        modeler = Modeler.objects.create(user=user, name="Test Modeler Name", project=project)
        dm = DM.objects.create(title="DM Name", project=project, creator=modeler, author=modeler, edited_by=modeler)
        self.assertNotEqual(dm.ct_id, "")
        self.assertNotEqual(dm.created, None)
        self.assertEqual(dm.published, False)
