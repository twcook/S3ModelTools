"""
Translator model definitions.
The translator allows for building a simple model to translate the data from a CSV file generated from a logical view, full table dump, etc. 
"""

import os
from time import time
import pytz

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.conf.global_settings import LANGUAGES as DJANGO_LANG

from dmgen.models import Project, Modeler, dm_folder, Attestation, Audit, XdLink

LANGUAGES = [('en-US', 'US English'), ('pt-BR', 'Brazilian Portuguese')]
for n in DJANGO_LANG:
    LANGUAGES.append(n)


def data_upload(instance, filename):
    """
    Name and location of uploaded search results.
    """
    tfolder = 'translator_csv'
    ts = str(int(time()))                     # the timestamp rounded to an integer when the file was uploaded
    ext = filename.split('.')[-1]             # reuse the original file extension
    path_file = os.path.join(tfolder, ts + '.' + ext)
    return path_file


class DMD(models.Model):
    """
     Data Model Description. This information is used to create a Data Model object with a Cluster that contains one eXtended Data Type for each column defined in the Records table.  
    """
    DELIM_CHOICES = ((',', _('Comma')), (';', _('Semicolon')), ('|', _('Pipe')), (':', _('Colon')))
    TZLIST = []
    for z in pytz.common_timezones_set:
        TZLIST.append((z,z))

    title = models.CharField(_('title'), unique=True, max_length=255, help_text=_("Enter the name of this Data Model."))
    project = models.ForeignKey(Project, verbose_name=_("project name"), to_field="prj_name", help_text=_('Choose a Project for this Data Model (DM). Projects are informal groupings that aide in tracking models.'), on_delete=models.CASCADE,)
    description = models.TextField(_('description'), help_text=_("Enter a general description for this DM."))
    definitions = models.TextField(_('definitions'), blank=False, help_text=_("Enter one or more URIs (prefereable URLs) that can be used as a definition / description for the data model. One per line."))
    author = models.ForeignKey(Modeler, verbose_name=_("Author"), help_text=_("Select the primary author of the DM"), related_name='%(class)s_related_author', on_delete=models.CASCADE,)
    contrib = models.ManyToManyField(Modeler, verbose_name=_("Contributors"), help_text=_("Select the contributors (if any) to this DM"), related_name='%(class)s_related_contrib', blank=True)

    subject = models.CharField(_('subject'), max_length=255, help_text=_("Enter a semi-colon separated list of keywords to help identify the usefulness and meaning of this concept."))
    source = models.CharField(_('source'), max_length=255, help_text=_("Enter the name of a document or a URL to a supporting source."))
    rights = models.CharField(_('rights'), max_length=255, help_text=_("Enter the rights or license statement."), default="CC-BY http://creativecommons.org/licenses/by/3.0/")
    relation = models.CharField(_('relation'), max_length=255, help_text=_("Enter the relationship to another Data Model (DM), if applicable."), default="None")
    coverage = models.CharField(_('coverage'), max_length=255, help_text=_("Enter the demographic, geographical or political coverage."), default="Universal")
    publisher = models.CharField(_('publisher'), max_length=255, help_text=_("Enter the name of the publisher/copyright holder."))
    pub_date = models.DateTimeField(verbose_name=_("date of publication"), auto_now=True, help_text=_("Date of publication."))
    dc_format = models.CharField(_('format'), max_length=8, editable=False, default="text/xml", help_text=_('The format of the data. Default is text/xml for DMs.'))

    delim = models.CharField( _('Delimiter'), max_length=1, choices=DELIM_CHOICES, default=",", help_text=_('If your CSV data is not using one of the supported formats it will need to be converted prior to translation, using an external tool.'))
    lang = models.CharField(_("language"), max_length=40, choices=LANGUAGES, default='en-US', help_text=_('Choose the language of this Data Model.'))
    default_tz = models.CharField(_("Default Timezone"), max_length=100, choices=TZLIST, default='UTC', help_text=_('Choose the default timezone for datatime definitions when it is missing from the data..'))
    data_gen = models.BooleanField(_('Generate XML?'), default=True, help_text=_('Check this box to automatically generate an XML dataset based on the generated model. If not checked only a model and sample files is generated.'))
    rdf_gen = models.BooleanField(_('Generate RDF?'), default=True, help_text=_('Check this box to automatically generate a RDF dataset based on the generated model and the data files. This will only function if the Generate Data box is also checked.'))

    csv_file = models.FileField("CSV Upload", upload_to=data_upload, max_length=2048, blank=True, null=True)

    audit = models.ManyToManyField(Audit, verbose_name=_('audit model(s)'), blank=True, help_text=_('Audit structure to provide audit trail tracking of information.'))
    attestation = models.ForeignKey(Attestation, verbose_name=_('attestation model'), null=True, blank=True, help_text=_('An attestation model used to affirm that this data is correct.'), on_delete=models.SET_NULL,)
    links = models.ManyToManyField(XdLink, verbose_name=_('link model(s)'), blank=True, related_name='%(class)s_related_links', default=None, help_text=_('Can be used to establish ad-hoc links between concepts.'))

    class Meta:
        verbose_name = "Data Model Definition"
        verbose_name_plural = "Data Model Definitions"

    def __str__(self):
        return self.title.strip()


class Record(models.Model):
    """
    A description of each column in the CSV file.
    The title returned is eXtended Datatype.
    """
    DT_CHOICES = (('xdstring', _('Text')), ('xdcount', _('Integer')), ('xdquantity', _('Decimal')), ('xdfloat', _('Float')), ('xdtemporal', _('Date/Time')))

    dmd = models.ForeignKey(DMD, verbose_name=_("Data Model Definition"), help_text=_('This is the associated Data Model Definition.'), on_delete=models.CASCADE,)
    header = models.CharField(_("Header"), max_length=110, help_text=_('The column header retrieved from the CSV file.'))
    label = models.CharField(_('label'), max_length=110, help_text=_("Initially this is the CSV column header. It should be changed to a human readable label used to describe this data."))
    description = models.TextField(_('description'), default='Description goes here.', help_text=_("Enter a general description for this datatype."))
    
    dt_type = models.CharField(_('datatype type'), max_length=20, choices=DT_CHOICES, help_text=_('Select the datatype for this column and then complete the constraints in the matching section below. For Floats, Integers and Decimals you must select the Numbers section and complete the Units (name and uri) fields.'))
    
    min_length = models.IntegerField(_('minimum length'), help_text=_("Enter the minimum number of characters that are required for this string. If the character is optional, leave it blank."), null=True, blank=True)
    
    max_length = models.IntegerField(_('maximum length'), help_text=_("Enter the maximum number of characters that are required for this string. If the character is optional, leave it blank."), null=True, blank=True)
    
    exact_length = models.IntegerField(_('exact length'), help_text=_("Enter the exact length of the string. It should be defined only when the number of characters is always fixed (e.g. codes and identifiers)."), null=True, blank=True)
    
    enums = models.TextField(_('enumerations'), blank=True, help_text=_("For text types that are restricted to one of a set of strings, enter the set of values of the string (e.g. Male, Female, Unknown). One per line."))
    
    def_val = models.CharField(_('default value'), max_length=255, blank=True, help_text=_("Enter a default value (up to 255 characters) for the string if desired. Cannot contain 'http://' nor 'https://'"))

    regex = models.CharField(_('pattern match'), max_length=255, blank=True, help_text=_("Is a pattern match required to validate this field? If so it should be expressed as a Regular Expression using the XML Schema regex dialect. See: http://www.xmlschemareference.com/regularExpression.html "))
    
    definitions = models.TextField(_('definitions'), blank=True, help_text=_("Enter one or more URIs (URLs are prefereable) that can be used as a reason, definition or description for the data in this column. One per line. These usually point to a controlled vocabulary but may only point to a PDF directive document."))
    
    min_magnitude = models.DecimalField(_('minimum magnitude'), blank=True, null=True, max_digits=10, decimal_places=5, help_text=_("The minimum allowed value for a magnitude. If there isn't a min. then leave blank."))
    
    max_magnitude = models.DecimalField(_('maximum magnitude'), blank=True, null=True, max_digits=10, decimal_places=5, help_text=_("Any maximum allowed value. If there isn't a max. then leave blank."))
    
    min_inclusive = models.DecimalField(_('minimum inclusive'), max_digits=10, decimal_places=5, help_text=_("Enter the minimum (inclusive) value for this concept."), null=True, blank=True)

    max_inclusive = models.DecimalField(_('maximum inclusive'), max_digits=10, decimal_places=5, help_text=_("Enter the maximum (inclusive) value for this concept."), null=True, blank=True)

    min_exclusive = models.DecimalField(_('minimum exclusive'), max_digits=10, decimal_places=5, help_text=_("Enter the minimum (exclusive) value for this concept."), null=True, blank=True)

    max_exclusive = models.DecimalField(_('maximum exclusive'), max_digits=10, decimal_places=5, help_text=_("Enter the maximum (exclusive) value for this concept."), null=True, blank=True)
    
    total_digits = models.IntegerField(_('total digits'), help_text=_("Enter the maximum number of digits for this concept, excluding the decimal separator and the decimal places."), null=True, blank=True)
    
    allow_duration = models.BooleanField(_('duration'), default=False, help_text=_("If a duration is allowed then no other temporal type is allowed."))
    
    allow_date = models.BooleanField(_('date'), default=False, help_text=_('Allow ISO dates: YYYY-MM-DD'))
    
    allow_time = models.BooleanField(_('time'), default=False, help_text=_('Allow ISO times: HH:MM:SS:dd'))
    
    allow_datetime = models.BooleanField(_('datetime'), default=False, help_text=_('Allow ISO DateTimes w/Timezone: YYYY-MM-DDTHH:MM:SS:ddZ. If the timezone is missing in the data then the defualt DMD timezone will be used.'))
    
    allow_day = models.BooleanField(_('day'), default=False, help_text=_('Allow: - - DD'))
    
    allow_month = models.BooleanField(_('month'), default=False, help_text=_('Allow: - MM -'))
    
    allow_year = models.BooleanField(_('year'), default=False, help_text=_('Allow:  YYYY- - '))
    
    allow_year_month = models.BooleanField(_('year month'), default=False, help_text=_('Allow: YYYY-MM-'))
    
    allow_month_day = models.BooleanField(_('month day'), default=False, help_text=_('Allow: - MM-DD'))
    
    units_name = models.CharField(_('Units Name'), max_length=255, blank=True, help_text=_("Enter the name of what is being counted or measured."))
    
    units_uri = models.CharField(_('Units URI'), max_length=255, blank=True, help_text=_("Enter a URI that defines this units designation."))

    def __str__(self):
        return self.dmd.title + ":" + self.label.strip()

    class Meta:
        ordering = ['dmd', 'header']
        verbose_name = "eXtended Datatype Definition"
        verbose_name_plural = "eXtended Datatype Definitions"

