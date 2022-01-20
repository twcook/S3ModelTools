"""
The S3Model Reference Model code to write DM schemas.
"""
import os
from datetime import date
import hashlib
import zipfile
from shutil import copy, rmtree
from xml.sax.saxutils import escape
from urllib.parse import quote
import json
import xmltodict
from lxml import etree

from django.core.files.base import ContentFile
from django.contrib import messages

from S3ModelTools.settings import DM_LIB, DM_PKG, MEDIA_ROOT, RMVERSION, RM_URI

from tools.models import NS, get_rcode
from tools.publisher import publish_DM

from .ig import cluster, Xd_link, party, participation, Xd_string, audit, attestation

from .fg import buildHTML


class DMPkg(object):
    """
    The class that collects all of the components for a DM package.
    A DM package consists of the DM (XML Schema), an XML instance, a JSON instance and an RStudio project.
    Also, the dm-description.xsl file is copied into the package from the root of the DM Library.
    """

    def __init__(self, dm, request):
        self.dm = dm
        self.request = request
        self.xsd = ''
        self.html = ''
        self.xml = ''
        self.ct_id = str(self.dm.ct_id).strip()
        self.used_uuids = {}
        self.clusters = []
        self.adapters = []
        self.dm.identifier = 'dm-' + str(self.dm.ct_id).strip()
        self.xsdHead = self.xsdHeader()
        self.xsdTail = '\n</xs:schema>\n'
        self.xmlHead = self.xmlHeader()
        self.xmlTail = '</s3m:dm-' + str(self.dm.ct_id).strip() + '>\n'
        self.xsdMetadata = self.xsdMetadata()
        self.rm = '<!-- Include the RM Schema -->\n  <xs:include schemaLocation="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION.replace('.', '_') + '.xsd"/>\n'
        self.msg = ("The DM complexType was generated.", messages.SUCCESS)

    def xmlHeader(self):
        """
        Build the header for the example instance
        """
        hstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
        hstr += '<s3m:dm-' + str(self.dm.ct_id).strip() + '\n'
        for ns in NS.objects.all():
            hstr += '  xmlns:' + ns.abbrev.strip() + '="' + ns.uri.strip() + '"\n'
        hstr += 'xsi:schemaLocation="https://www.s3model.com/ns/s3m/  https://tools.s3model.com/dmlib/dm-' + str(self.dm.ct_id).strip() + '.xsd">\n'
        return(hstr)

    def xsdHeader(self):
        """
        Build the header string for the XSD
        """
        hstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
        hstr += '<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>\n'
        hstr += '<xs:schema\n'
        for ns in NS.objects.all():
            hstr += '  xmlns:' + ns.abbrev.strip() + '="' + ns.uri.strip() + '"\n'
        hstr += '  targetNamespace="https://www.s3model.com/ns/s3m/"\n'
        hstr += '  xml:lang="' + self.dm.dc_language.strip() + '">\n'
        return(hstr)

    def xsdMetadata(self):
        mds = '<!-- Metadata -->\n  <xs:annotation><xs:appinfo><rdf:RDF><rdf:Description\n'
        mds += '    rdf:about="dm-' + str(self.dm.ct_id) + '">\n'
        mds += '    <dc:title>' + escape(self.dm.title.strip()) + '</dc:title>\n'
        mds += '    <dc:creator>' + escape(self.dm.author.__str__()) + '</dc:creator>\n'
        if len(self.dm.contrib.all()) != 0:
            for c in self.dm.contrib.all():
                mds += '    <dc:contributor>' + escape(c.__str__()) + '</dc:contributor>\n'
        mds += '    <dc:dc_subject>' + escape(self.dm.dc_subject.strip()) + '</dc:dc_subject>\n'
        mds += '    <dc:rights>' + escape(self.dm.rights) + '</dc:rights>\n'
        mds += '    <dc:relation>' + escape(self.dm.relation.strip()) + '</dc:relation>\n'
        mds += '    <dc:coverage>' + escape(self.dm.coverage.strip()) + '</dc:coverage>\n'
        mds += '    <dc:type>' + escape(self.dm.dc_type.strip()) + '</dc:type>\n'
        mds += '    <dc:identifier>' + escape(self.dm.identifier.strip()) + '</dc:identifier>\n'
        mds += '    <dc:description>' + escape(self.dm.description.strip()) + '</dc:description>\n'
        mds += '    <dc:publisher>' + escape(self.dm.publisher.strip()) + '</dc:publisher>\n'
        mds += '    <dc:date>' + str(self.dm.pub_date) + '</dc:date>\n'
        mds += '    <dc:format>' + escape(self.dm.dc_format.strip()) + '</dc:format>\n'
        mds += '    <dc:language>' + escape(self.dm.dc_language.strip()) + '</dc:language>\n'
        mds += '  </rdf:Description></rdf:RDF></xs:appinfo></xs:annotation>\n'
        return(mds)

    def registerUUID(self, uuid, rmtype, sg, mc_name):
        """
        Register all of the UUIDs used for MCs in the DM. Insure that each complexType is included only one time.
        For XSD 1.0 compatibility each component can only have one substitutionGroup.
        uuid is a string representation of the UUID.
        rmtype is a string representing the RM type.
        sg is a string representing the substitutionGroup needed.
        """
        new = True
        if uuid in self.used_uuids.keys():
            new = False
            if self.used_uuids[uuid][0][1] is not None:
                if self.used_uuids[uuid][0] != (rmtype, sg):  # used for XSD 1.0
                    self.xsd = None
                    self.published = False
                    self.msg = ("ERROR: The component " + mc_name + " -- " + rmtype + " cannot be used in multiple places for different functions. Please create a new component for one of those uses.", messages.ERROR)
                    return(new)

            # self.used_uuids[uuid].append((rmtype, sg))  # used for XSD 1.1 to allow multiple substitution groups
        else:
            self.used_uuids[uuid] = [(rmtype, sg)]
        return(new)

    def processDM(self):
        self.msg = ("The DM complexType was generated.", messages.SUCCESS)

        self.msg = self.dm.publish(self.request)

        self.xsd += self.dm.schema_code  # the DM complexType
        indent = ""
        link_str = ''

        self.xml += """<label>""" + self.dm.title + """</label>\n"""
        self.xml += """<dm-language>""" + self.dm.language + """</dm-language>\n"""
        self.xml += """<dm-encoding>""" + self.dm.encoding + """</dm-encoding>\n"""
        self.xml += """<current-state>""" + self.dm.state + """</current-state>\n"""

        # links - we need to process links first because a XdLink 'could' be
        # reused in a later Cluster and we need to insure it gets a
        # substitution group
        if self.dm.links.all():
            for link in self.dm.links.all():
                if self.registerUUID(link.ct_id, 'XdLinkType', 'XdLink', link.label):
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)

                    self.xsd += link.schema_code
                    # we put the XdLink instance info in a temp string and
                    # add it at the bottom of the Entry
                    link_str += Xd_link(link, indent)
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)

        # data
        if self.dm.data:
            if self.registerUUID(self.dm.data.ct_id, 'ClusterType', 'Item', self.dm.data.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += self.dm.data.schema_code
                self.msg = self.processCluster(self.dm.data)
                self.xml += cluster(self.dm.data, indent)
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
        else:
            self.msg = ("The DM is missing a Data (ClusterType) model.", messages.ERROR)
            return(self.msg)

        # subject
        if self.dm.subject:
            if self.registerUUID(self.dm.subject.ct_id, 'PartyType', None, self.dm.subject.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += self.dm.subject.schema_code
                self.xml += "<subject>\n"
                self.xml += party(self.dm.subject, indent)
                self.xml += "</subject>\n"
                self.msg = self.processParty(self.dm.subject)
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

        # provider
        if self.dm.provider:
            if self.registerUUID(self.dm.provider.ct_id, 'PartyType', None, self.dm.provider.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += self.dm.provider.schema_code
                self.xml += "<provider>\n"
                self.xml += party(self.dm.provider, indent)
                self.xml += "</provider>\n"
                self.msg = self.processParty(self.dm.provider)
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

        # participations
        if self.dm.participations.all():
            for part in self.dm.participations.all():
                if self.registerUUID(part.ct_id, 'ParticipationType', 'Participation', part.label):
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)

                    self.xsd += part.schema_code
                    self.xml += participation(part, indent)
                    self.msg = self.processParticipation(part)
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)

        # protocol
        if self.dm.protocol:
            if self.registerUUID(self.dm.protocol.ct_id, 'XdStringType', None, self.dm.protocol.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += self.dm.protocol.schema_code
                self.xml += "<protocol>\n"
                self.xml += Xd_string(self.dm.protocol, indent, False)
                self.xml += "</protocol>\n"

        # workflow
        if self.dm.workflow:
            if self.registerUUID(self.dm.workflow.ct_id, 'XdLinkType', None, self.dm.workflow.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += self.dm.workflow.schema_code
                self.xml += "<workflow>\n"
                self.xml += Xd_link(self.dm.workflow, indent, False)
                self.xml += "</workflow>\n"

        # audit
        if self.dm.audit.all():
            for aud in self.dm.audit.all():
                if self.registerUUID(aud.ct_id, 'AuditType', 'Audit', aud.label):
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)

                    self.xsd += aud.schema_code
                    self.xml += audit(aud, indent)
                    self.msg = self.processAudit(aud)
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)

        # attestation
        if self.dm.attestation:
            if self.registerUUID(self.dm.attestation.ct_id, 'AttestationType', None, self.dm.attestation.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += self.dm.attestation.schema_code
                self.msg = self.processAttestation(self.dm.attestation)
                self.xml += "<attestation>\n"
                self.xml += attestation(self.dm.attestation, indent)
                self.xml += "</attestation>\n"
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

        # add the XdLink string to the XML instance
        self.xml += link_str
        return(self.msg)

    def processCluster(self, cluster):
        self.msg = ("Processed " + cluster.label, messages.SUCCESS)

        # Clusters
        for clust in cluster.clusters.all():
            self.clusters.append(clust.ct_id)
            # first check for Cluster loops that cannot be resolved.
            if self.clusters.count(clust.ct_id) > 100:
                self.msg = ("I think the tools is in a loop because you have embedded a Cluster inside itself on some level, OR there are more than 100 embedded Clusters, which seems kind of ridiculous.", messages.ERROR)
                return(self.msg)

            # register the clusters
            if self.registerUUID(clust.ct_id, 'ClusterType', 'Items', clust.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                self.xsd += clust.schema_code
                self.msg = self.processCluster(clust)
                if msg[1] == messages.ERROR:
                    return(self.msg)

        # XdBooleans in Cluster
        for Xd in cluster.xdboolean.all():
            if self.registerUUID(Xd.ct_id, 'XdBooleanType', 'XdAdapter-value', Xd.label):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdBoolean: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code   # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdLinks in Cluster
        for Xd in cluster.xdlink.all():
            if self.registerUUID(Xd.ct_id, 'XdLinkType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdLink: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code   # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdStrings in Cluster
        for Xd in cluster.xdstring.all():
            if self.registerUUID(Xd.ct_id, 'XdStringType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdString: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code  # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdFiles in Cluster
        for Xd in cluster.xdfile.all():
            if self.registerUUID(Xd.ct_id, 'XdFileType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdFile: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code   # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdOrdinals in Cluster
        for Xd in cluster.xdordinal.all():
            if self.registerUUID(Xd.ct_id, 'XdOrdinalType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdOrdinal: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code   # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange', Xd.label):
                            if self.msg[1] == messages.ERROR:
                                return(self.msg)
                            if len(rr.schema_code) < 10:
                                self.msg = ("Something happened to your MC code. Check that ReferenceRange: " + rr.label + " is published.", messages.ERROR)
                                return(self.msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType', 'XdInterval', rr.interval.label):
                                if self.msg[1] == messages.ERROR:
                                    return(self.msg)
                                if len(rr.interval.schema_code) < 10:
                                    self.msg = ("Something happened to your MC code. Check that XdInterval: " + rr.interval.label + " is published.", messages.ERROR)
                                    return(self.msg)
                                self.xsd += rr.interval.schema_code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdCounts in Cluster
        for Xd in cluster.xdcount.all():
            if self.registerUUID(Xd.ct_id, 'XdCountType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)

                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdCount: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code  # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            if self.msg[1] == messages.ERROR:
                                return(self.msg)
                            if len(rr.schema_code) < 10:
                                self.msg = ("Something happened to your MC code. Check that ReferenceRange: " + rr.label + " is published.", messages.ERROR)
                                return(self.msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                if self.msg[1] == messages.ERROR:
                                    return(self.msg)
                                if len(rr.interval.schema_code) < 10:
                                    self.msg = ("Something happened to your MC code. Check that XdInterval: " + rr.interval.label + " is published.", messages.ERROR)
                                    return(self.msg)
                                self.xsd += rr.interval.schema_code
                if Xd.units:
                    if self.registerUUID(Xd.units.ct_id, 'Units', None, Xd.units.label):
                        if self.msg[1] == messages.ERROR:
                            return(self.msg)
                        if len(Xd.units.schema_code) < 10:
                            self.msg = ("Something happened to your MC code. Check that Units: " + Xd.units.label + " is published.", messages.ERROR)
                            return(self.msg)
                        self.xsd += Xd.units.schema_code
                else:
                    self.msg = ("Your XdCount is missing a Xdcount-units value. This should have been a publishing error; <b>Contact the tools authors</b>.", messages.ERROR)
                    return(self.msg)
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdQuantities in Cluster
        for Xd in cluster.xdquantity.all():
            if self.registerUUID(Xd.ct_id, 'XdQuantityType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdQuanitiy: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code  # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            if self.msg[1] == messages.ERROR:
                                return(self.msg)
                            if len(rr.schema_code) < 10:
                                self.msg = ("Something happened to your MC code. Check that ReferenceRange: " + rr.label + " is published.", messages.ERROR)
                                return(self.msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                if self.msg[1] == messages.ERROR:
                                    return(self.msg)
                                if len(rr.interval.schema_code) < 10:
                                    self.msg = ("Something happened to your MC code. Check that XdInterval: " + rr.interval.label + " is published.", messages.ERROR)
                                    return(self.msg)
                                self.xsd += rr.interval.schema_code
                if Xd.units:
                    if self.registerUUID(Xd.units.ct_id, 'Units', None, Xd.units.label):
                        if self.msg[1] == messages.ERROR:
                            return(self.msg)
                        if len(Xd.units.schema_code) < 10:
                            self.msg = ("Something happened to your MC code. Check that Units: " + Xd.units.label + " is published.", messages.ERROR)
                            return(self.msg)
                        self.xsd += Xd.units.schema_code
                else:
                    self.msg = ("Your XdQuantity is missing a Xdquantity-units value. This should have been a publishing error; <b>Contact the tools authors</b>.", messages.ERROR)
                    return(self.msg)
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdRatios in Cluster
        for Xd in cluster.xdratio.all():
            if self.registerUUID(Xd.ct_id, 'XdRatioType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdRatio: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code   # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            if self.msg[1] == messages.ERROR:
                                return(self.msg)
                            if len(rr.schema_code) < 10:
                                self.msg = ("Something happened to your MC code. Check that ReferenceRange: " + rr.label + " is published.", messages.ERROR)
                                return(self.msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                if self.msg[1] == messages.ERROR:
                                    return(self.msg)
                                if len(rr.interval.schema_code) < 10:
                                    self.msg = ("Something happened to your MC code. Check that XdInterval: " + rr.interval.label + " is published.", messages.ERROR)
                                    return(self.msg)
                                self.xsd += rr.interval.schema_code
                if Xd.num_units:
                    if self.registerUUID(Xd.num_units.ct_id, 'Units', None, Xd.units.label):
                        if self.msg[1] == messages.ERROR:
                            return(self.msg)
                        if len(Xd.num_units.schema_code) < 10:
                            self.msg = ("Something happened to your MC code. Check that Units: " + Xd.num_units.label + " is published.", messages.ERROR)
                            return(self.msg)
                        self.xsd += Xd.num_units.schema_code
                if Xd.den_units:
                    if self.registerUUID(Xd.den_units.ct_id, 'Units', None, Xd.units.label):
                        if self.msg[1] == messages.ERROR:
                            return(self.msg)
                        if len(Xd.den_units.schema_code) < 10:
                            self.msg = ("Something happened to your MC code. Check that Units: " + Xd.den_units.label + " is published.", messages.ERROR)
                            return(self.msg)
                        self.xsd += Xd.den_units.schema_code

                if Xd.ratio_units:
                    if self.registerUUID(Xd.ratio_units.ct_id, 'Units', None, Xd.units.label):
                        if self.msg[1] == messages.ERROR:
                            return(self.msg)
                        if len(Xd.ratio_units.schema_code) < 10:
                            self.msg = ("Something happened to your MC code. Check that Units: " + Xd.ratio_units.label + " is published.", messages.ERROR)
                            return(self.msg)
                        self.xsd += Xd.ratio_units.schema_code

            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdTemporals in Cluster
        for Xd in cluster.xdtemporal.all():
            if self.registerUUID(Xd.ct_id, 'XdTemporalType', 'XdAdapter-value', Xd.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(Xd.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdTemporall: " + Xd.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += Xd.schema_code   # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange', Xd.label):
                            if self.msg[1] == messages.ERROR:
                                return(self.msg)
                            if len(rr.schema_code) < 10:
                                self.msg = ("Something happened to your MC code. Check that ReferenceRange: " + rr.label + " is published.", messages.ERROR)
                                return(self.msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType', None, Xd.label):
                                if self.msg[1] == messages.ERROR:
                                    return(self.msg)
                                if len(rr.interval.schema_code) < 10:
                                    self.msg = ("Something happened to your MC code. Check that XdInterval: " + rr.interval.label + " is published.", messages.ERROR)
                                    return(self.msg)
                                self.xsd += rr.interval.schema_code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id, Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        return(self.msg)

    def processParty(self, party):
        self.msg = ("Processed Party " + party.label, messages.SUCCESS)

        if party.external_ref.all():
            for ref in party.external_ref.all():
                if self.registerUUID(ref.ct_id, 'XdLinkType', None, ref.label):
                    if self.msg[1] == messages.ERROR:
                        return(self.msg)
                    if len(ref.schema_code) < 10:
                        self.msg = ("Something happened to your MC code. Check that XdLink: " + ref.label + " is published.", messages.ERROR)
                        return(self.msg)
                    self.xsd += ref.schema_code

        if party.details:
            if self.registerUUID(party.details.ct_id, 'ClusterType', None, party.details.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(party.details.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that Cluster: " + party.details.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += party.details.schema_code
                self.msg = self.processCluster(party.details)

        return(self.msg)

    def processParticipation(self, part):
        self.msg = ("Processed Participation " + part.label, messages.SUCCESS)

        if part.performer:
            if self.registerUUID(part.performer.ct_id, 'PartyType', None, part.performer.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(part.performer.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that Party: " + part.performer.label + " is published.", messages.ERROR)
                self.xsd += part.performer.schema_code
                self.msg = self.processParty(part.performer)

        if part.function:
            if self.registerUUID(part.function.ct_id, 'XdStringType', None, part.function.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(part.function.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdString: " + part.function.label + " is published.")
                    return(self.msg)
                self.xsd += part.function.schema_code

        if part.mode:
            if self.registerUUID(part.mode.ct_id, 'XdStringType', None, part.mode.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(part.mode.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdString: " + part.mode.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += part.mode.schema_code

        return(self.msg)

    def processAudit(self, aud):
        self.msg = ("Processed Audit " + aud.label, messages.SUCCESS)

        if aud.system_id:
            if self.registerUUID(aud.system_id.ct_id, 'XdStringType', None, aud.system_id.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(aud.system_id.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdString: " + aud.system_id.label + " is published.", messages.ERROR)
                self.xsd += aud.system_id.schema_code

        if aud.system_user:
            if self.registerUUID(aud.system_user.ct_id, 'PartyType', None, aud.system_user.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(aud.system_user.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that Party: " + aud.system_user.label + " is published.")
                    return(self.msg)
                self.xsd += aud.system_user.schema_code
                self.msg = self.processParty(aud.system_user)

        if aud.location:
            if self.registerUUID(aud.location.ct_id, 'ClusterType', None, aud.location.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(aud.location.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that Cluster: " + aud.location.label + " is published.", messages.ERROR)
                    return(self.msg)
                self.xsd += aud.location.schema_code
                self.msg = self.processCluster(aud.location)

        return(self.msg)

    def processAttestation(self, att):
        self.msg = ("Processed Attestation " + att.label, messages.SUCCESS)

        if att.view:
            if self.registerUUID(att.view.ct_id, 'XdFileType', None, att.view.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(att.view.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdFile: " + att.view.label + " is published.", messages.ERROR)
                self.xsd += att.view.schema_code

        if att.proof:
            if self.registerUUID(att.proof.ct_id, 'XdFileType', None, att.proof.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(att.proof.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdFile: " + att.proof.label + " is published.", messages.ERROR)
                self.xsd += att.proof.schema_code

        if att.reason:
            if self.registerUUID(att.reason.ct_id, 'XdStringType', None, att.reason.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(att.reason.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that XdString: " + att.reason.label + " is published.", messages.ERROR)
                self.xsd += att.reason.schema_code

        if att.committer:
            if self.registerUUID(att.committer.ct_id, 'PartyType', None, att.committer.label):
                if self.msg[1] == messages.ERROR:
                    return(self.msg)
                if len(att.committer.schema_code) < 10:
                    self.msg = ("Something happened to your MC code. Check that Party: " + att.committer.label + " is published.")
                    return(self.msg)
                self.xsd += att.committer.schema_code
                self.msg = self.processParty(att.committer)

        return(self.msg)

    def makeXdAdapter(self, ct_id, adapter_id, xd_name):
        """
        Create an adapter for a complexType when used in a Cluster.
        Requires the ct_id of the complexType and the pre-generated adapter ct_id for that datatype.
        Returns the string.
        """
        adr_str = ''
        indent = 2
        padding = ('').rjust(indent)

        # Create the Adapter
        adr_str += padding.rjust(indent) + ("<xs:element name='ms-" + adapter_id + "' substitutionGroup='s3m:Items' type='s3m:mc-" + adapter_id + "'/>\n")
        adr_str += padding.rjust(indent) + ("<xs:complexType name='mc-" + adapter_id + "'> <!-- Adapter for: " + escape(xd_name) + " -->\n")
        adr_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
        adr_str += padding.rjust(indent + 4) + ("<xs:restriction base='s3m:XdAdapterType'>\n")
        adr_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
        adr_str += padding.rjust(indent + 8) + ("<xs:element  maxOccurs='unbounded' minOccurs='0' ref='s3m:ms-" + ct_id + "'/> <!-- Reference to: " + escape(xd_name) + " -->\n")
        adr_str += padding.rjust(indent + 6) + ("</xs:sequence>\n")
        adr_str += padding.rjust(indent + 4) + ("</xs:restriction>\n")
        adr_str += padding.rjust(indent + 2) + ("</xs:complexContent>\n")
        adr_str += padding.rjust(indent) + ("</xs:complexType>\n")

        return adr_str

    def processSubstitutionGroups(self):
        """
        Only one substitution group is allowed in XSD 1.0 so if a complexType is used in more than one place throw an error and stop generation.
        The original code allows for multiple substitution groups once we can support XSD 1.1. At that time remove the check for sg_names length.
        """
        self.msg = ("Substitution Groups generated.", messages.SUCCESS)

        self.xsd += '\n<!-- Substitution Groups -->\n'
        for uuid in self.used_uuids.keys():
            sg_names = []

            for n in range(0, len(self.used_uuids[uuid])):
                if self.used_uuids[uuid][n][1] is not None:  # check for a substitution group
                    if 's3m:' + self.used_uuids[uuid][n][1] not in sg_names:
                        sg_names.append('s3m:' + self.used_uuids[uuid][n][1])

            if len(self.used_uuids[uuid]) > 1:
                self.msg = ("ERROR generating substitution groups for: " + uuid + " -- " + str(self.used_uuids[uuid]), messages.ERROR)
                return(self.msg)

            sg_str = 'substitutionGroup="' + " ".join(sg_names)
            if len(sg_names) > 0:
                self.xsd += ('  <xs:element name="ms-' + str(uuid) + '" ' + sg_str + '" type="s3m:mc-' + str(uuid) + '"/>\n')
        return(self.msg)

    def rmcRDF(self):
        self.msg = ("RMC RDF was generated.", messages.SUCCESS)

        self.xsd += '\n<!-- RDF for contained Reusable Model Components -->\n'
        self.xsd += "  <xs:annotation>\n"
        self.xsd += "  <xs:appinfo>\n"

        for uuid in self.used_uuids:
            self.xsd += '      <rdf:Description rdf:about="dm-' + str(self.dm.ct_id) + '">\n'
            self.xsd += '        <s3m:containsRMC rdf:resource="mc-' + str(uuid) + '"/>\n'
            self.xsd += '      </rdf:Description>\n'

        self.xsd += "  </xs:appinfo>\n"
        self.xsd += "  </xs:annotation>\n"

        return(self.msg)

    def getXSD(self):
        """
        The method that initiates building the XML Schema and the XML example instance.
        """
        self.msg = ("The schema was generated.", messages.SUCCESS)

        self.xsd += self.xsdHead
        self.xsd += self.rm
        self.xsd += self.xsdMetadata
        self.xsd += '<!-- Complex Type Definitions -->\n'

        self.xml += self.xmlHead
        # start building the DM and the XML instance
        self.msg = self.processDM()

        # create the substitution groups, add RDF for contained MCs and close the schema and instance
        if self.msg[1] == messages.SUCCESS:
            self.msg = self.processSubstitutionGroups()
            if self.msg[1] == messages.ERROR:
                return(self.msg)

            self.msg = self.rmcRDF()
            if self.msg[1] == messages.ERROR:
                return(self.msg)

        if self.msg[1] == messages.SUCCESS:
            self.xsd += self.xsdTail
            self.xml += self.xmlTail

        return(self.msg)


def generateDM(dm, request):
    """
    Called from the DMAdmin in admin.py.
    This function triggers building the objects used to define the content for output.
    """

    # Cleanup - Remove old files if this DM has been generated before.
    # Set Published as false.
    dm.html_file.delete()
    dm.xml_file.delete()
    dm.json_file.delete()
    dm.xsd_file.delete()
    dm.sha1_file.delete()
    dm.zip_file.delete()
    dm.published = False
    dm.save()

    ns_dict = {}
    for ns in NS.objects.all():
        ns_dict[ns.abbrev.strip()] = ns.uri.strip()

    # begin processing
    dmpkg = DMPkg(dm, request)
    dmpkg.getXSD()
    if dmpkg.msg[1] == messages.ERROR:
        dm.published = False
        dm.schema_code = None
        dm.save()
        return(dmpkg.msg)

    # build the HTML form
    dmpkg = buildHTML(dmpkg)

    # set the umask so we can create files in the directory we create via
    # Apache/NGINX.
    prevumask = os.umask(0o000)

    # create a unique directory based on the DM Title in the Package directory
    pkg_dir = DM_PKG
    fldr_title = ''.join([c for c in dm.title if c.isalnum() and ord(c) <= 127])
    dm_dir = pkg_dir + "/" + fldr_title
    if os.path.exists(dm_dir):
        rmtree(dm_dir)

    os.makedirs(dm_dir, 0o777)

    if dmpkg.msg[1] == messages.SUCCESS:
        # write the files

        # open a schema file dm-(uuid).xsd
        f = ContentFile(dmpkg.xsd.encode("utf-8"))
        xsd = dm.xsd_file
        xsd.save('dm-' + str(dm.ct_id) + '.xsd', f, save=True)
        xsd.flush()
        dm.xsd_file.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.xsd', os.O_RDWR | os.O_CREAT)
        os.write(lf, dmpkg.xsd.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS, "Wrote the DM schema file.")
        # copy the schema to the dmlib directory
        copy(dm_dir + '/dm-' + str(dm.ct_id) + '.xsd', DM_LIB + '/dm-' + str(dm.ct_id) + '.xsd')

        # copy the style sheet to used in displaying the thml form
        copy(pkg_dir + '/dm-description.xsl', dm_dir + '/dm-description.xsl')

        # open an HTML file dm-(uuid).html
        f = ContentFile(dmpkg.html.encode("utf-8"))
        html = dm.html_file
        html.save('dm-' + str(dm.ct_id) + '.html', f, save=True)
        html.flush()
        dm.html_file.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.html', os.O_RDWR | os.O_CREAT)
        os.write(lf, dmpkg.html.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS, "Wrote the HTML form file.")

        # open an instance file dm-(uuid).xml
        f = ContentFile(dmpkg.xml.encode("utf-8"))
        xml = dm.xml_file
        xml.save('dm-' + str(dm.ct_id) + '.xml', f, save=True)
        xml.flush()
        dm.xml_file.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.xml', os.O_RDWR | os.O_CREAT)
        os.write(lf, dmpkg.xml.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS, "Wrote the XML Instance file.")

        """
         open and write a JSON instance file dm-(uuid).json
        """

        f = ContentFile(dmpkg.xml.encode("utf-8"))  # this is the XML instance before conversion
        xmldict = xmltodict.parse(f, process_namespaces=True, namespaces=ns_dict)
        j = json.dumps(xmldict, indent=2)
        jfile = ContentFile(j)
        jsonfile = dm.json_file
        jsonfile.save('dm-' + str(dm.ct_id) + '.json', jfile)
        jsonfile.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.json', os.O_RDWR | os.O_CREAT)
        os.write(lf, j.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS, "Wrote the JSON Instance file.")

        """
        generate and write the SHA1 file
        """
        dmxsd = open(dm_dir + '/dm-' + str(dm.ct_id) + '.xsd', encoding="utf-8")
        dm_content = dmxsd.read()
        dmxsd.close()
        h = hashlib.sha1(dm_content.encode("utf-8")).hexdigest()
        f = ContentFile(h)
        sha1 = dm.sha1_file
        sha1.save('dm-' + str(dm.ct_id) + '.sha1', f)
        sha1.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.sha1', os.O_RDWR | os.O_CREAT)
        os.write(lf, h.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS, "Wrote the SHA1 digital signature file.")

        """
        Generate the RDF from the semantics embeded in the XSD.
        """

        parser = etree.XMLParser(ns_clean=True, recover=True)
        cls_def = etree.XPath("//xs:annotation/xs:appinfo/rdfs:Class", namespaces=ns_dict)
        md = etree.XPath("//rdf:RDF/rdf:Description", namespaces=ns_dict)
        sh_def = etree.XPath("//xs:annotation/xs:appinfo/sh:property", namespaces=ns_dict)

        rdf_file = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.rdf', os.O_RDWR | os.O_CREAT)

        rdfstr = """<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n"""

        tree = etree.parse(ContentFile(dmpkg.xsd.encode("utf-8")), parser)
        root = tree.getroot()

        rdf = cls_def(root)
        shacl = sh_def(root)

        for m in md(root):
            rdfstr += '    ' + etree.tostring(m).decode('utf-8') + '\n'

        for r in rdf:
            rdfstr += '    ' + etree.tostring(r).decode('utf-8') + '\n'

        for s in shacl:
            rdfstr += '    ' + etree.tostring(s).decode('utf-8') + '\n'

        rdfstr += '</rdf:RDF>\n'
        os.write(rdf_file, rdfstr.encode("utf-8"))
        os.close(rdf_file)
        messages.add_message(request, messages.SUCCESS,
                             "Wrote the RDF for the DM.")

        """
        create ZIP of the directory and the JSON, html, xsd, xml, sha1 files and the R project
        """
        zf = zipfile.ZipFile(MEDIA_ROOT + '/dm-' + str(dm.ct_id) + '.zip', 'w')
        for dirname, subdirs, files in os.walk(dm_dir):
            for filename in files:
                zf.write(os.path.join(dirname, filename),
                         dirname.replace('../dmlib/', '') + '/' + filename)

        zf.close()
        messages.add_message(request, messages.SUCCESS,
                             "Created a ZIP of all the files.")

        os.umask(prevumask)  # reset the umask

        dm.published = True
        dm.save()

    return(dmpkg.msg)

