import time

from cuid import cuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf.global_settings import LANGUAGES as DJANGO_LANG
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages

from tools.models import Project, Modeler
# import all of the publishers.
from .publisher import (publish_XdBoolean, publish_XdLink, publish_XdString, publish_XdFile, publish_XdInterval,
                        publish_ReferenceRange, publish_SimpleReferenceRange, publish_XdOrdinal, publish_XdCount, publish_XdQuantity, publish_XdFloat,
                        publish_XdTemporal, publish_Party, publish_Participation, publish_Audit, publish_Attestation,
                        publish_Cluster, publish_DM)

LANGUAGES = [('en-US', 'US English'), ('pt-BR', 'Brazilian Portuguese')]
for n in DJANGO_LANG:
    LANGUAGES.append(n)

def get_cuid():
    # insure there are no collisions
    time.sleep(.001)
    return cuid()

def dm_folder(instance, filename):
    fldr_title = ''.join(
        [c for c in instance.title if c.isalnum() and ord(c) <= 127])
    return '/'.join([fldr_title, filename])

# no one should be able to delete a published object
@receiver(pre_delete)
def no_delete_test(sender, instance, **kwargs):
    if sender in [Cluster, XdBoolean, XdString, XdCount, XdString, XdInterval, XdFile, XdOrdinal, XdQuantity, XdFloat, XdString, XdTemporal, XdLink, Participation, Party, ReferenceRange, Units]:
        if instance.published:
            raise PermissionDenied


class Namespace(models.Model):
    """
    Namespace abbreviations and URIs are used to define the relationships between Model Components and the outside world.
    The namespace abbreviation and the namespace URI are defined in the Namespace table.
    """
    ns_abbrev = models.CharField(("Namespace Abbreviation"), max_length=30, help_text=('Enter a namespace abbreviation.'), unique=True)
    ns_uri = models.CharField(("Namespace URI"), default="", max_length=2000, help_text=('Enter the namespace URI for the abbreviation.'), unique=True)

    def __str__(self):
        return self.ns_abbrev + " --> " + self.ns_uri.strip()

    class Meta:
        ordering = ['ns_abbrev']
        verbose_name = "Namespace"
        verbose_name_plural = "Namespaces"


class SemanticLink(models.Model):
    """
    Semantic links are used to define the relationships between Model Components and the outside world.
    They are expressed in the Data Model as RDF triples; Subject, Predicate, Object (SPO).
    The Subject is the Model Component being defined.
    The Predicate is the relationship between the Subject and the Object. It consists of a namespace abbreviation and a classname.
    The Object is the external resource that the Model Component is related to via the predicate.
    The namespace abbreviation and the namespace URI are defined in the Namespace table.
    """
    sl_name = models.CharField(("Name"), max_length=100, help_text=("Enter a human readable name for this Semantic Link. This is only used to aide selection, it is not part of the MC semantics."), blank=False, default='')
    namespace = models.ForeignKey(Namespace, verbose_name=("Namespace"), help_text=("Select a namespace to define the RDF triple."), blank=True, null=True, on_delete=models.SET_NULL,)
    class_name = models.CharField(("Classname"), max_length=50, help_text=('Enter a valid classname from the vocabulary.'), blank=False, default='')
    

    def __str__(self):
        return self.sl_name.strip()

    class Meta:
        ordering = ['sl_name']
        verbose_name = "Semantic Link"
        verbose_name_plural = "Semantic Links"


class Common(models.Model):
    """
    Columns common to all entries except DM.
    """
    project = models.ForeignKey(Project, verbose_name=("Project Name"), to_field="prj_name", help_text=('Choose the name of your Project.'), on_delete=models.CASCADE,)
    public = models.BooleanField(("Is Public?"), default=True, help_text=("Public components are available to every other modeller. If not public then the component is only visible within the project it was defined in."))
    label = models.CharField(('label'), max_length=110, help_text=("A human readable label used to identify this model in DMGEN. This will also be use in generated app UI."))
    ct_id = models.CharField(("CUID"), max_length=40, default=get_cuid, editable=False, unique=True, help_text=('The unique identifier for the MC.'))
    created = models.DateTimeField(('created'), auto_now_add=True, blank=False, help_text=('The dateTime that the MC was created.'))
    updated = models.DateTimeField(('last updated'), auto_now=True, help_text=("Last update."))
    published = models.BooleanField(("published"), default=False, help_text=("Published must be a green check icon in order to use this in a DM. This is not user editable. It is managed by the publication process."))
    description = models.TextField(('description'), help_text=("Enter a free text description for this complexType. Include a usage statement and any possible misuses. This is used as the annotation for the MC and as help text in the UI."), null=True)
    sem_links = models.ManyToManyField(SemanticLink, verbose_name=("Semantic Links"), blank=True, help_text=("Select or create a new set of semantic links to define this item."))
    schema_code = models.TextField(("Schema Code"), help_text="This is only writable from the DMGEN, not via user input. It contains the code required for each component to create an entry in a DM.", blank=True, null=True, default='')
    lang = models.CharField(("language"), max_length=40, choices=LANGUAGES, default='en-US', help_text=('Choose the language of this MC.'))
    creator = models.ForeignKey(Modeler, verbose_name="Creator", blank=True, related_name='%(class)s_related_creator', default=1, on_delete=models.SET_DEFAULT,)
    edited_by = models.ForeignKey(Modeler, verbose_name="Last Edited By", blank=True, related_name='%(class)s_related_edited_by', default=1, on_delete=models.SET_DEFAULT,)
    seq = models.CharField(("Sequence Number"), max_length=4, default='0000', help_text=('Enter the sequence number (aka. TabIndex) for this component in the UI. Components nested in a Cluster are grouped together. When two or more components have the same number they will be sorted by label.'))
    validate = models.BooleanField(("Hard Validate?"), default=False, help_text=("Hard validation is when the UI enforces criteria on input fields. Soft validation allows users to input any value, warns them when it is not within parameters of the component. Then offers to allow correction or select an Exceptional Value as explaination."))
    app_code = models.TextField(("App Code"), help_text="This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.", blank=True, null=True, default='')



    def __str__(self):
        return self.project.prj_name + ' : ' + self.label

    class Meta:
        abstract = True
        ordering = ['project', 'label']
        indexes = [models.Index(fields=['project', 'label']),]


class XdAny(Common):
    """
    Abstract root of all datatypes.
    """
    UI_TYPES = (('choose', 'Choose Type:'), ('input', 'Input Box'), ('dropdown', 'Dropdown'), ('radiogroup', 'Radio Button Group'), ('radio', 'Radio Button'), ('checkbox', 'Checkbox(es)') )

    adapter_ctid = models.CharField(("CUID"), max_length=40, default=get_cuid, editable=False, unique=True, help_text=('This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.'))
    require_act = models.BooleanField(('Access Control Tag'), default=False, help_text=('Check this box to require an Access Control Tag element.'))
    require_vtb = models.BooleanField(('Valid Time Begin'), default=False, help_text=('Check this box to require a Valid Time Begin element.'))
    require_vte = models.BooleanField(('Valid Time End'), default=False, help_text=('Check this box to require a Valid Time End element.'))
    require_tr = models.BooleanField(('Time Recorded'), default=False, help_text=('Check this box to require a Date & Time Recorded element.'))
    require_mod = models.BooleanField(('Time Modified'), default=False, help_text=('Check this box to require a Date & Time for last modified element.'))
    require_location = models.BooleanField(('Location'), default=False, help_text=('Check this box to require a decimal longitude and latitude location.'))
    ui_type = models.CharField(("Preferred UI Type"), max_length=40, choices=UI_TYPES, default='Choose UI Type:', help_text=('Choose the preferred UI Type for this component. Use UX best practices. Be aware that the generator may override your selection.'))
    allow_vtb = models.BooleanField(('Allow Valid Time Begin?'), default=False, help_text=('Check this box to allow a Valid Time Begin element even when not required.'))
    allow_vte = models.BooleanField(('Allow Valid Time End?'), default=False, help_text=('Check this box to allow a Valid Time End element even when not required.'))
    allow_tr = models.BooleanField(('Allow Time Recorded?'), default=False, help_text=('Check this box to allow a Date & Time Recorded element even when not required.'))
    allow_mod = models.BooleanField(('Allow Time Modified?'), default=False, help_text=('Check this box to allow a Date & Time for last modified element even when not required.'))
    allow_location = models.BooleanField(('Allow Location?'), default=False, help_text=('Check this box to allow a decimal longitude and latitude location even when not required.'))

    class Meta:
        abstract = True
        ordering = ['label']


class XdBoolean(XdAny):
    """
    Items which represent boolean decisions, such as true/false or yes/no answers. Use for such data, it
    is important to devise the meanings (usually questions in subjective data) carefully, so that the only allowed results
    are in fact true or false.

    Potential MisUse: The XdBoolean class should not be used as a replacement for naively
    modelled enumerated types such as male/female etc. Such values should be coded, and in any case the enumeration often
    has more than two values.
    """
    trues = models.TextField(('true values'), help_text=("Enter the set of values that are Boolean TRUEs. For instance, if this is a 'Yes/No' type of concept, usually the 'Yes' is a Boolean TRUE. Enter one per line."))
    falses = models.TextField(('false values'), help_text=("Enter the set of values that are Boolean FALSEs. For instance, if this is a 'Yes/No' type of concept, usually the 'No' is a Boolean FALSE. Enter one per line."))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdBoolean(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Boolean"
        verbose_name_plural = "Booleans"
        ordering = ['project', 'label']


class XdLink(XdAny):
    """
    Used to specify a link to another resource such as another DM.
    """
    link = models.CharField(('Link URI'), max_length=255, help_text=("The Link URI that points to the linked item."))
    relation = models.CharField(('Relationship'), max_length=110, help_text=("The relationship describing the link. Usually constrained by an ontology such as <a href='https://github.com/oborel/obo-relations'>OBO RO</a>."))
    relation_uri = models.CharField(('Relationship URI'), max_length=255, help_text=("The relationship URI. Points to the vocabulary, ontology, etc that provides the relation."))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdLink(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        ordering = ['project', 'label']


class XdString(XdAny):
    """
    The string data type may contain characters, line feeds, carriage returns, and tab characters.
    Used to constrain strings to an enumerated set or may be used for free text entry.
    When defining constraints the publisher has this sequence of priorities: Enumeration, Exact Length, Max & Min Lengths, Min Length, Max Length, Default value.
    """
    min_length = models.IntegerField(('minimum length'), help_text=("Enter the minimum number of characters that are required for this string. If the character is optional, leave it blank."), null=True, blank=True)
    max_length = models.IntegerField(('maximum length'), help_text=("Enter the maximum number of characters that are required for this string. If the character is optional, leave it blank."), null=True, blank=True)
    exact_length = models.IntegerField(('exact length'), help_text=("Enter the exact length of the string. It should be defined only when the number of characters is always fixed (e.g. codes and identifiers)."), null=True, blank=True)
    enums = models.TextField(('enumerations'), blank=True, help_text=("Enter the set of values of the string (e.g.Male,Female). One per line."))
    definitions = models.TextField(('enumeration definitions'), blank=True, help_text=("Enter a URI (prefereable a URL) defining each enumeration. One per line. If the URI is the same for each enumeration then just put it on the first line."))
    def_val = models.CharField(('default value'), max_length=255, blank=True, help_text=("Enter a default value (up to 255 characters) for the string if desired. Cannot contain 'http://' nor 'https://'. Notice that if other restrictions are used, this default is ignored."))
    str_fmt = models.CharField(('String Format'), max_length=60, blank=True, help_text=("Enter a regular expression used to constrain the string to a specific format. See the XML reduced regex set here: https://www.regular-expressions.info/xml.html "))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdString(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "String"
        verbose_name_plural = "Strings"
        ordering = ['project', 'label']


class Units(XdAny):
    """
    An XdString data type used to define Units for Quantified types.
    """
    min_length = models.IntegerField(('minimum length'), help_text=("Enter the minimum number of characters that are required for this concept. If the character is optional, leave it blank."), null=True, blank=True)
    max_length = models.IntegerField(('maximum length'), help_text=("Enter the maximum number of characters that are required for this concept. If the character is optional, leave it blank."), null=True, blank=True)
    exact_length = models.IntegerField(('exact length'), help_text=("Enter the exact length of the concept. It should be defined only when the number of characters is always fixed (e.g. codes and identifiers)."), null=True, blank=True)
    enums = models.TextField(('Symbols'), help_text=("Enter the abbreviations or symbols for allowed units designations. One per line."))
    def_val = models.CharField(('default value'), max_length=255, blank=True, help_text=("Enter a default value (up to 255 characters) for the string if desired. Cannot contain 'http://' nor 'https://'"))
    definitions = models.TextField(('Symbol definitions'), help_text=("Enter a URI for each symbol. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all symbols then enter it on the first line only."))
    str_fmt = models.CharField(('String Format'), max_length=60, blank=True, help_text=("Enter a regular expression used to constrain the string to a specific format. See the XML reduced regex set here: https://www.regular-expressions.info/xml.html "))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdString(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)
        return msg

    class Meta:
        verbose_name = "Units"
        verbose_name_plural = "Units"
        ordering = ['project', 'label']


class XdFile(XdAny):
    """
    Used to define external files that may be included directly or by reference.
    """
    MODE_TYPES = (('select', 'Select Mode:'), ('url', 'Link via a URL'), ('embed', 'Embed a file'))
    media_type = models.TextField(("Media Type"), help_text=("The allowed Media Types (formerly known as MIME Types) of the included data, one per line; i.e. text/html"), blank=True)
    encoding = models.CharField(("encoding"), max_length=10, default='utf-8', help_text=("<a href='http://www.iana.org/assignments/character-sets/character-sets.txt'>List of encoding types at IANA.</a>"))
    language = models.CharField(("default language"), max_length=40, choices=LANGUAGES, default='en-US', help_text=('Choose the DEFAULT language of the content.'))
    alt_txt = models.CharField(("Alt. Text"), max_length=110, blank=True, help_text=('Default alternative text label to display when the content cannot be displayed.'))
    content_mode = models.CharField(("Content Mode"), default='Select Mode:', help_text=("Select how the content will referenced, either via a URL or included in the data instance."), choices=MODE_TYPES, max_length=6)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdFile(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "File"
        ordering = ['project', 'label']


class XdInterval(XdAny):
    """
    Generic class defining an interval (i.e. range) of a comparable type. An interval is a contiguous
    subrange of a comparable base type. Used to define intervals of dates, times, quantities Whose units of measure match
    and datatypes are the same and are ordered. See http://docstore.mik.ua/orelly/xml/schema/ch04_04.htm for value limits on numerics.
    """
    INTERVAL_TYPES = (('None', 'Select Type:'), ('int', 'Count data (xs:int)'), ('decimal', 'Real set numbers (xs:decimal)'), ('float', 'Floating Point (xs:float)'),
                      ('dateTime', 'Date/Time (YYYY-MM-DDTHH:mm:ss)'), ('date', 'Date (YYYY-MM-DD)'), ('time', 'Time (HH:mm:ss)'), ('duration', 'Duration (xs:duration)'))

    lower = models.CharField(("Lower Value"), max_length=110, blank=True, null=True, help_text=('Enter the lower value of the interval. This will be used to set the minInclusive facet.'))
    upper = models.CharField(("Upper Value"), max_length=110, blank=True, null=True, help_text=('Enter the upper value of the interval. This will be used to set the maxInclusive facet.'))
    interval_type = models.CharField(("Interval Type"), default='Select Type:', help_text=("The XML Schema datatype of the upper and lower values."), choices=INTERVAL_TYPES, max_length=20)
    lower_included = models.BooleanField(('Lower Included?'), default=True, help_text=('Uncheck this box if the lower value is excluded in the interval'))
    upper_included = models.BooleanField(('Upper Included?'), default=True, help_text=('Uncheck this box if the upper value is excluded in the interval'))
    lower_bounded = models.BooleanField(('Lower Bounded?'), default=True, help_text=("Uncheck this box if the lower value is unbounded. If unchecked, instances must be set to xsi:nil='true'"))
    upper_bounded = models.BooleanField(('Upper Bounded?'), default=True, help_text=("Uncheck this box if the lower value is unbounded. If unchecked, instances must be set to xsi:nil='true'"))
    units_name = models.CharField(("Units Name"), max_length=60, blank=True, null=True, help_text=('OPTIONAL: Enter the common name or abbreviation for these units.'))
    units_uri = models.URLField(("Units URI"), max_length=2000, blank=True, null=True, help_text=('Enter the URL pointing to the definition for these units. This is mandatory if you entered a Units Name.'))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdInterval(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip(
            ) + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Interval"
        ordering = ['project', 'label']


class ReferenceRange(XdAny):
    """
    Defines a named range to be associated with any ORDERED datum.

    """

    definition = models.CharField(("Definition"), max_length=110, help_text=("Enter the term that indicates the status of this range, e.g. 'normal', 'critical', 'therapeutic' etc."))
    interval = models.ForeignKey(XdInterval, verbose_name=('interval'), help_text=("The data range for this meaning. Select the appropriate XdInterval."), on_delete=models.CASCADE,)
    is_normal = models.BooleanField(('Is Normal?'), default=False, help_text=("Is this considered the normal range?"))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_ReferenceRange(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "ReferenceRange"
        ordering = ['project', 'label']


class SimpleReferenceRange(XdAny):
    """
    Defines a ReferenceRange with one and only one Interval included.
    The Interval is a simple type from the XSD type system. This is the most common type of ReferenceRange.
    """

    INTERVAL_TYPES = (('None', 'Select Type:'), ('int', 'Count data (xs:int)'), ('decimal', 'Real set numbers (xs:decimal)'), ('float', 'Floating Point (xs:float)'), ('dateTime', 'Date/Time (YYYY-MM-DDTHH:mm:ss)'), ('date', 'Date (YYYY-MM-DD)'), ('time', 'Time (HH:mm:ss)'), ('duration', 'Duration (xs:duration)'))

    definition = models.CharField(("Definition"), max_length=110, help_text=("Enter the term that indicates the status of this range, e.g. 'normal', 'critical', 'therapeutic' etc."))
    lower = models.CharField(("Lower Value"), max_length=110, blank=True, null=True, help_text=('Enter the lower value of the interval. This will be used to set the minInclusive facet.'))
    upper = models.CharField(("Upper Value"), max_length=110, blank=True, null=True, help_text=('Enter the upper value of the interval. This will be used to set the maxInclusive facet.'))
    interval_type = models.CharField(("Interval Type"), default='Select Type:', help_text=("The XML Schema datatype of the upper and lower values."), choices=INTERVAL_TYPES, max_length=20)
    lower_included = models.BooleanField(('Lower Included?'), default=True, help_text=('Uncheck this box if the lower value is excluded in the interval'))
    upper_included = models.BooleanField(('Upper Included?'), default=True, help_text=('Uncheck this box if the upper value is excluded in the interval'))
    lower_bounded = models.BooleanField(('Lower Bounded?'), default=True, help_text=("Uncheck this box if the lower value is unbounded. If unchecked, instances must be set to xsi:nil='true'"))
    upper_bounded = models.BooleanField(('Upper Bounded?'), default=True, help_text=("Uncheck this box if the lower value is unbounded. If unchecked, instances must be set to xsi:nil='true'"))
    units_name = models.CharField(("Units Name"), max_length=60, blank=True, null=True, help_text=('OPTIONAL: Enter the common name or abbreviation for these units.'))
    units_uri = models.URLField(("Units URI"), max_length=2000, blank=True, null=True, help_text=('Enter the URL pointing to the definition for these units. This is mandatory if you entered a Units Name.'))
    is_normal = models.BooleanField(('Is Normal?'), default=False, help_text=("Is this considered the normal range?"))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_SimpleReferenceRange(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "ReferenceRange (Simple)"
        verbose_name_plural = "ReferenceRanges (Simple)"
        ordering = ['project', 'label']


class XdOrdered(XdAny):
    """
    Abstract class defining the concept of ordered values, which includes ordinals as well as true
    quantities. The implementations require the functions ‘&lt;’, '&gt;' and is_strictly_comparable_to ('==').
    """
    reference_ranges = models.ManyToManyField(ReferenceRange, verbose_name=('reference ranges'), blank=True, help_text=('Select the appropriate ReferenceRange that defines each ordered value. The listing is by Project: Reference Range Name.'))
    normal_status = models.CharField(('normal status'), max_length=110, help_text=("Enter text that indicates a normal status. Example: This should be a Symbol in a XdOrdinal, a date range in a XdTemporal, a value range in a XdCount, etc."), blank=True, null=True)
    simple_rr = models.ForeignKey(SimpleReferenceRange, verbose_name=("Reference Range (Simple)"), null=True, blank=True, on_delete=models.SET_NULL)

    def publish(self):
        pass

    class Meta:
        abstract = True


class XdOrdinal(XdOrdered):
    """
    Models rankings and scores, e.g. pain, Apgar values, etc, where there is:
    a) implied ordering,
    b) no implication that the distance between each value is constant, and
    c) the total number of values is finite.
    Note that although the term ‘ordinal’ in mathematics means natural numbers only, here any decimal is allowed, since negative and
    zero values are often used by medical and other professionals for values around a neutral point. Also, decimal values are
    sometimes used such as 0.5 or .25
    Examples of sets of ordinal values:
    -3, -2, -1, 0, 1, 2, 3 -- reflex response values
    0, 1, 2 -- Apgar values
    Used for recording any clinical datum which is customarily recorded using symbolic values.
    Example: the results on a urinalysis strip, e.g. {neg, trace, +, ++, +++} are used for leucocytes, protein, nitrites
    etc; for non-haemolysed blood {neg, trace, moderate}; for haemolysed blood {neg, trace, small, moderate, large}.
    """
    ordinals = models.TextField(('ordinals'), help_text=("Enter the ordered enumeration of values. The base integer is zero with any number of integer values used to order the symbols. Example A: 0 = Trace, 1 = +, 2 = ++, 3 = +++, etc. Example B: 0 = Mild, 1 = Moderate, 2 = Severe. One per line."))
    symbols = models.TextField(('symbols'), help_text=("Enter the symbols or the text that represent the ordinal values, which may be strings made from '+' symbols, or other enumerations of terms such as 'mild', 'moderate', 'severe', or even the same number series used for the ordinal values, e.g. '1', '2', '3'.. One per line."))
    annotations = models.TextField(('Symbols Definitions'), blank=True, help_text=("Enter a URI for as a definition for each symbol. One per line. If the URI is the same for each symbol then just put it on the first line."))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdOrdinal(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Ordinal"
        ordering = ['project', 'label']


class XdTemporal(XdOrdered):
    """
    Class defining the concept of date and time types.
    Must be constrained in DMs to be one or more of the allowed types.
    This gives the modeller the ability to optionally allow partial dates at run time.
    If one of the duration types is selected then no other type is allowed.
    All types are considered optional (minOccurs='0') by default.
    If you need to make on mandatory then an assert statement is required and only one type should be allowed.
    """
    allow_duration = models.BooleanField(('allow duration'), default=False, help_text=("If Duration is allowed, no other types will be permitted."))
    allow_date = models.BooleanField(('allow date'), default=False, help_text=('Check this box if complete date entry is allowed.'))
    allow_time = models.BooleanField(('allow time'), default=False, help_text=('Check this box if time only entry is allowed.'))
    allow_datetime = models.BooleanField(('allow datetime'), default=False, help_text=('Check this box if complete dates and times are allowed.'))
    allow_day = models.BooleanField(('allow day'), default=False, help_text=('Check this box if day only is allowed.'))
    allow_month = models.BooleanField(('allow month'), default=False, help_text=('Check this box if month only is allowed.'))
    allow_year = models.BooleanField(('allow year'), default=False, help_text=('Check this box if year only entry is allowed.'))
    allow_year_month = models.BooleanField(('allow year month'), default=False, help_text=('Check this box if combination of years and months are allowed.'))
    allow_month_day = models.BooleanField(('allow month day'), default=False, help_text=('Check this box if combination of months and days are allowed.'))

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdTemporal(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Temporal"
        ordering = ['project', 'label']


class XdQuantified(XdOrdered):
    """
    Abstract class defining the concept of true quantified values, i.e. values which are not only ordered,
    but which have a precise magnitude.
    """
    min_magnitude = models.DecimalField(('minimum magnitude'), blank=True, null=True, max_digits=10, decimal_places=5, help_text=("The minimum allowed value for a magnitude. If there isn't a min. then leave blank."))
    max_magnitude = models.DecimalField(('maximum magnitude'), blank=True, null=True, max_digits=10, decimal_places=5, help_text=("Any maximum allowed value. If there isn't a max. then leave blank."))
    min_inclusive = models.DecimalField(('minimum inclusive'), max_digits=10, decimal_places=5, help_text=("Enter the minimum (inclusive) value for this concept."), null=True, blank=True)
    max_inclusive = models.DecimalField(('maximum inclusive'), max_digits=10, decimal_places=5, help_text=("Enter the maximum (inclusive) value for this concept."), null=True, blank=True)
    min_exclusive = models.DecimalField(('minimum exclusive'), max_digits=10, decimal_places=5, help_text=("Enter the minimum (exclusive) value for this concept."), null=True, blank=True)
    max_exclusive = models.DecimalField(('maximum exclusive'), max_digits=10, decimal_places=5, help_text=("Enter the maximum (exclusive) value for this concept."), null=True, blank=True)
    total_digits = models.IntegerField(('total digits'), help_text=("Enter the maximum number of digits for this concept, excluding the decimal separator and the decimal places."), null=True, blank=True)
    require_ms = models.BooleanField(('Require Magnitude Status?'), default=False, help_text=('MagnitudeStatus provides a general indication of the accuracy of the magnitude expressed in the XdQuantified subtypes. Should be used to inform users and not for decision support uses.'))
    require_error = models.BooleanField(('Require Error Value?'), default=False, help_text=('Error margin of measurement, indicating error in the recording method or instrument (+/- %). A logical value of 0 indicates 100% accuracy, i.e. no error.'))
    require_accuracy = models.BooleanField(('Require Accuracy Value?'), default=False, help_text=('Accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. A value of 0 means that the accuracy is unknown.'))
    allow_ms = models.BooleanField(('Allow Magnitude Status?'), default=False, help_text=('Allow a UI component for this element even if it is not required.'))
    allow_error = models.BooleanField(('Allow Error Value?'), default=False, help_text=('Allow a UI component for this element even if it is not required.'))
    allow_accuracy = models.BooleanField(('Allow Accuracy Value?'), default=False, help_text=('Allow a UI component for this element even if it is not required.'))

    def publish(self):
        pass

    class Meta:
        abstract = True


class XdCount(XdQuantified):
    """
    Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy
    patient), number of cigarettes smoked in a day, etc. Misuse:Not used for amounts of physical entities (which all have
    standardized units)
    """
    units = models.ForeignKey(Units, verbose_name=('units'), related_name='%(class)s_related_units', null=True, help_text=("Choose a units of measurement of this concept."), on_delete=models.SET_NULL,)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdCount(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Count"
        ordering = ['project', 'label']


class XdQuantity(XdQuantified):
    """
    Quantitified type representing “scientific” quantities, i.e. quantities expressed as a magnitude (decimal) and
    units. Can also be used for time durations, where it is more convenient to treat these as simply a number of individual
    seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.
    """
    fraction_digits = models.IntegerField(('fraction digits'), help_text=("Enter the maximum number of decimal places."), null=True, blank=True)
    units = models.ForeignKey(Units, verbose_name=('units'), related_name='%(class)s_related_units', null=True, help_text=("Choose a units of measurement of this concept."), on_delete=models.SET_NULL,)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdQuantity(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Quantity"
        verbose_name_plural = "Quantities"
        ordering = ['project', 'label']

class XdFloat(XdQuantified):
    """
    Quantitified type representing “scientific” quantities, i.e. quantities expressed as a magnitude (float) and an optional units.
    """
    units = models.ForeignKey(Units, verbose_name=('units'), related_name='%(class)s_related_units', null=True, help_text=("Choose a units of measurement of this concept."), on_delete=models.SET_NULL,)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_XdFloat(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Float"
        verbose_name_plural = "Floats"
        ordering = ['project', 'label']


class Party(Common):
    """
    A proxy description of a party, including an optional link to data for this party in a demographic or other identity management system.
    """
    details = models.ForeignKey('Cluster', verbose_name=('details'), related_name='%(class)s_related', null=True, blank=True, help_text=('A Cluster structure that defines the details of this Party.'), on_delete=models.SET_NULL,)
    external_ref = models.ManyToManyField(XdLink, verbose_name=('external reference'), help_text=("Optional XdLink(s) that point to a description of this Party in other services."), blank=True, related_name='%(class)s_related')

    class Meta:
        verbose_name = "Party"
        ordering = ['project', 'label']

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_Party(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg


class Audit(Common):
    """
    Audit provides a mechanism to identifiy the who/where/when tracking of instances as they move from system to system.
    """
    system_id = models.ForeignKey(XdString, verbose_name=('system id'), null=True, blank=True, related_name='%(class)s_related', help_text=('Identifier of the system which handled the information item.'), on_delete=models.SET_NULL,)
    system_user = models.ForeignKey(Party, verbose_name=('system user'), null=True, blank=True, related_name='%(class)s_related', help_text=('A model for user(s) who created, committed, forwarded or otherwise handled the item.'), on_delete=models.SET_NULL,)
    location = models.ForeignKey('Cluster', verbose_name=('location'), related_name='%(class)s_related', null=True, blank=True, help_text=('A Cluster for location information.'), on_delete=models.SET_NULL,)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_Audit(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Audit"
        verbose_name_plural = "Audits"
        ordering = ['project', 'label']


class Attestation(Common):
    """
    Record an attestation by a party of item(s) of record content.
    The type of attestation is recorded by the reason attribute, which my be coded from a vocabulary.
    """
    view = models.ForeignKey(XdFile, verbose_name=('attested view'), related_name='attested_view', null=True, blank=True, help_text=('Select a model for the recorded view that is being attested.'), on_delete=models.SET_NULL,)
    proof = models.ForeignKey(XdFile, verbose_name=('proof'), related_name='proof', null=True, blank=True, help_text=('Select a model for the proof of attestation such as an GPG signature.'), on_delete=models.SET_NULL,)
    reason = models.ForeignKey(XdString, verbose_name=('reason'), related_name='%(class)s_related', null=True, blank=True, help_text=('Select a model for the reason.'), on_delete=models.SET_NULL,)
    committer = models.ForeignKey(Party, verbose_name=('committer'), related_name='%(class)s_related_committer', null=True, blank=True, help_text=('The Party that commited the Attestation.'), on_delete=models.SET_NULL,)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_Attestation(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Attestation"
        ordering = ['project', 'label']


class Participation(Common):
    """
    Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity,
    which is not explicitly in the model, e.g. assisting nurse, ambulance service, etc. Can be used to record past or future participations.
    """
    performer = models.ForeignKey(Party, verbose_name='Performer', related_name='%(class)s_related_performer', null=True, help_text=('The Party instance and possibly demographic system link of the party participating in the activity.'), on_delete=models.SET_NULL,)
    function = models.ForeignKey(XdString, related_name='%(class)s_related', null=True, help_text=('The function of the Party in this participation (note that a given party might participate in more than one way in a particular activity). In some applications this might be called a Role.'), on_delete=models.SET_NULL,)
    mode = models.ForeignKey(XdString, related_name='%(class)s_related_mode', null=True, help_text=('The mode of the performer / activity interaction, e.g. present, by telephone, by email etc. If the participation is by device or software it may contain a protocol standard or interface definition.'), on_delete=models.SET_NULL,)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_Participation(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Participation"
        ordering = ['project', 'label']


class Cluster(Common):
    """
    The grouping structure of Item, which may contain further instances of Item subclasses, in an ordered list. This
    provides the root Item for potentially very complex structures.
    """
    clusters = models.ManyToManyField('Cluster', help_text="Select zero or more Clusters to include in this Cluster. You cannot put a Cluster inside itself, it will be ignored if you select itself.", blank=True)
    xdboolean = models.ManyToManyField(XdBoolean, verbose_name='Boolean', related_name='%(class)s_related', help_text="Select zero or more booleans to include in this Cluster.", blank=True)
    xdlink = models.ManyToManyField(XdLink, verbose_name='Link', related_name='%(class)s_related', help_text="Select zero or more uris to include in this Cluster.", blank=True)
    xdstring = models.ManyToManyField(XdString, verbose_name='String', related_name='%(class)s_related', help_text="Select zero or more strings to include in this Cluster.", blank=True)
    xdfile = models.ManyToManyField(XdFile, verbose_name='File', related_name='%(class)s_related', help_text="Select zero or more media items to include in this Cluster.", blank=True)
    xdordinal = models.ManyToManyField(XdOrdinal, verbose_name='Ordinal', related_name='%(class)s_related', help_text="Select zero or more ordinals to include in this Cluster.", blank=True)
    xdcount = models.ManyToManyField(XdCount, verbose_name='Count', related_name='%(class)s_related', help_text="Select zero or more counts to include in this Cluster.", blank=True)
    xdquantity = models.ManyToManyField(XdQuantity, verbose_name='Quantity', related_name='%(class)s_related', help_text="Select zero or more quantity items to include in this Cluster.", blank=True)
    xdfloat = models.ManyToManyField(XdFloat, verbose_name='Float', related_name='%(class)s_related', help_text="Select zero or more floats to include in this Cluster.", blank=True)
    xdtemporal = models.ManyToManyField(XdTemporal, verbose_name='Temporal', related_name='%(class)s_related', help_text="Select zero or more temporal items to include in this Cluster.", blank=True)

    def publish(self, request):
        if self.schema_code == '':
            msg = publish_Cluster(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.label.strip() + ' was not published because code already exists.', messages.ERROR)

        return msg

    class Meta:
        verbose_name = "Cluster"
        ordering = ['label']


class DM(models.Model):
    """
    This is the root node of a Data Model.
    """
    ct_id = models.CharField(("CUID"), max_length=40, default=get_cuid, editable=False, unique=True, help_text=('The unique identifier for the DM.'))
    created = models.DateTimeField(('Created'), auto_now_add=True, help_text=('The dateTime that the MC was created.'))
    updated = models.DateTimeField(('Last updated'), auto_now=True, help_text=("Last update."))
    creator = models.ForeignKey(Modeler, verbose_name='Creator', related_name='%(class)s_related_creator', on_delete=models.CASCADE,)
    edited_by = models.ForeignKey(Modeler, verbose_name='Last Edited By', related_name='%(class)s_related_edited_by', on_delete=models.CASCADE,)
    published = models.BooleanField(("Generated"), default=False, help_text=("Once this <em>Generated</em> box has been checked, DM generation has been completed and no further edits are allowed."))
    project = models.ForeignKey(Project, verbose_name=("Project name"), to_field="prj_name", help_text=('Choose a Project for this Data Model (DM)'), on_delete=models.CASCADE,)
    about = models.CharField(('About'), default="http://dmgen.s3model.com/dmlib/", max_length=255, help_text=("The URL to the DM after publication. The DM ID will be added after the trailing slash in the format of 'dm-{dm_id}.xsd' This provides a full path and filename for the dm as a unique identifier."), blank=True)
    title = models.CharField(('Title'), unique=True, max_length=255, help_text=("Enter the name of this Data Model (DM)."))
    author = models.ForeignKey(Modeler, verbose_name=("Author"), help_text=("Select the author of the DM"), related_name='%(class)s_related_author', blank=True, on_delete=models.CASCADE,)
    contrib = models.ManyToManyField(Modeler, verbose_name=("Contributors"), help_text=("Select the contributors (if any) to this DM"), related_name='%(class)s_related_contrib', blank=True)
    dc_subject = models.CharField(('DC Subject'), max_length=255, default='', help_text=("Enter a semi-colon separated list of keywords. Usually MeSH terms"), blank=True)
    source = models.CharField(('DC Source'), max_length=255, default='', help_text=("Enter the name of a document or a URL to a supporting source."), blank=True)
    rights = models.CharField(('DC Rights'), max_length=255, help_text=("Enter the rights or license statement."), default="CC-BY http://creativecommons.org/licenses/by/3.0/", blank=True)
    relation = models.CharField(('DC Relation'), max_length=255, help_text=("Enter the relationship to another Data Model (DM), if applicable."), default="None", blank=True)
    coverage = models.CharField(('DC Coverage'), max_length=255, help_text=("Enter the demographic, geographical or political coverage."), default="Universal", blank=True)
    dc_type = models.CharField(('DC Type'), max_length=110, editable=False, default="S3Model Data Model (DM)")
    identifier = models.CharField(('DC Identifier'), max_length=110, editable=False, default="dm-")
    description = models.TextField(('Description'), help_text=("Enter a general description of the purpose of this DM."), blank=True)
    publisher = models.CharField(('DC Publisher'), max_length=255, help_text=("Enter the name of the publisher/copyright holder."), blank=True)
    pub_date = models.DateTimeField(verbose_name=("date of publication"), auto_now=True, help_text=("Date of publication."), blank=True)
    dc_format = models.CharField(('DC Format'), max_length=8, editable=False, default="text/xml", help_text=('The format of the data. Default is text/xml for DMs.'))
    dc_language = models.CharField(("DC Language"), max_length=7, default="en-US", choices=LANGUAGES, help_text=('The written language of the DM.'), blank=True)

    language = models.CharField(("Language"), max_length=40, choices=LANGUAGES, blank=True, default='en-US', help_text=('Choose the language of this Data Model.'))
    encoding = models.CharField(("Encoding"), max_length=10, default='utf-8', help_text="<a href='http://www.iana.org/assignments/character-sets/character-sets.txt'>List of encoding types at IANA.</a>")
    state = models.CharField(('Current State'), max_length=110, blank=True, help_text=('The current state according to the state machine / workflow engine identified in workflow_id. You may enter a default/start state here.'))
    data = models.ForeignKey(Cluster, verbose_name=('Model Data'), related_name='%(class)s_related', help_text=("You must select the Cluster that is the structure for this model."), null=True, on_delete=models.CASCADE,)
    subject = models.ForeignKey(Party, verbose_name=('Model Subject'), related_name='%(class)s_related_subject', null=True, blank=True, help_text=('Refers to the subject component of the record for anonymous or identified reference.'), on_delete=models.SET_NULL,)
    provider = models.ForeignKey(Party, verbose_name=('Model Provider'), related_name='%(class)s_related_provider', null=True, blank=True, help_text=('Select a Party componet that models the provider of the activity in this model.'), on_delete=models.SET_NULL,)
    participations = models.ManyToManyField(Participation, verbose_name=('Other Participations'), blank=True, help_text=('Select any Participations components that describe additional entities involved in this model.'))
    protocol = models.ForeignKey(XdString, null=True, verbose_name=('Protocol ID'), blank=True, help_text=('Optional external identifier of protocol used to create this Entry.  This could be a clinical guideline, an operations protocol,etc.'), on_delete=models.SET_NULL,)
    workflow = models.ForeignKey(XdLink, null=True, verbose_name=('Workflow ID'), blank=True, help_text=('Identifier of externally held workflow engine (state machine) data for this workflow execution.'), on_delete=models.SET_NULL,)
    acs = models.ForeignKey(XdLink, null=True, verbose_name=('ACS ID'), blank=True, related_name='%(class)s_access', help_text=('Identifier of externally held access control system. This URI can be an ontology, vocabulary or descriptive document; URI link.'), on_delete=models.SET_NULL,)
    audit = models.ManyToManyField('Audit', verbose_name=('Audit'), blank=True, help_text=('Audit structure to provide audit trail tracking of information.'))
    attestation = models.ForeignKey(Attestation, verbose_name=('Attestation'), null=True, blank=True, help_text=('A model that allows an attestation that the data is correct.'), on_delete=models.SET_NULL,)
    links = models.ManyToManyField(XdLink, verbose_name=('Links'), blank=True, related_name='%(class)s_related_links', default=None, help_text=('Can be used to establish ad-hoc links between concepts.'))

    asserts = models.TextField(("asserts"), help_text="XPath assert statements. See the documentation for details. One per line.", blank=True)
    sem_links = models.ManyToManyField(SemanticLink, verbose_name=("Semantic Links"), help_text=("Select or create a new set of semantic links."), blank=True)
    schema_code = models.TextField(("Schema Code"),  help_text="This is only writable from the DMGEN, not via user input. It contains the code required for each component to create an entry in a DM.", default='', blank=True, null=True, editable=True)
    doc_code = models.TextField(("Documentation Code"), help_text="This is only writable from the DMGEN, not via user input. It contains the HTML code to document the DM.", null=True,  blank=True)
    app_code = models.TextField(("App Code"), help_text="This is only writable from the DMGEN, not via user input. It contains the code required to create the User App.", blank=True, null=True, default='')
    xsd_file = models.FileField("DM XSD Schema", upload_to=dm_folder, max_length=2048, blank=True, null=True)
    xml_file = models.FileField("DM XML Instance", upload_to=dm_folder, max_length=2048, blank=True, null=True)
    json_file = models.FileField("DM JSON Instance", upload_to=dm_folder, max_length=2048, blank=True, null=True)
    html_file = models.FileField("DM HTML Form", upload_to=dm_folder, max_length=2048, blank=True, null=True)
    sha1_file = models.FileField("DM SHA1", upload_to=dm_folder, max_length=2048, blank=True, null=True)
    zip_file = models.FileField("DM Zip", upload_to='zips/', max_length=2048, blank=True, null=True)

    def __init_(self, *args, **kwargs):
        super(DM, self).__init_(*args, **kwargs)
        if self.ct_id:
            self.identifier = "dm-" + str(self.ct_id)

    def __str__(self):
        return self.project.prj_name + ' : ' + self.title

    def publish(self, request):
        if "(***COPY***)" in self.title:  # skip publishing a copy.
            msg = (self.title + " --Cannot publish a copy until it is edited.", messages.ERROR)
            return(msg)
        if self.schema_code == '' or self.schema_code == None:
            msg = publish_DM(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.schema_code = ''
                self.save()
        else:
            msg = (self.title.strip() + ' was not published because code already exists.', messages.ERROR)

        return(msg)

    class Meta:
        verbose_name = "DataModel"
        ordering = ['project', 'title']
        indexes = [models.Index(fields=['project', 'title']),]


