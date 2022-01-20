from django.db import models

"""
Models used by the CSV Modeler app.
"""

class XMLstore(models.Model):
    """
    Define XML data storage locations.
    """

    dbtype = models.CharField('Storage Type', max_length = 40, help_text = "")
    name = models.CharField('Storage Name', max_length = 250, help_text = "")
    host = models.CharField('Host Name', max_length = 500, help_text = "")
    port = models.CharField('Port Number', max_length = 10, help_text = "")
    dbname = models.CharField('Database Name', max_length = 250, help_text = "")
    user = models.CharField('User Name', max_length = 250, help_text = "")
    pw = models.CharField('User Password', max_length = 250, help_text = "")
    hostip = models.CharField('Host IP', max_length = 45, help_text = "")
    forests = models.PositiveSmallIntegerField(verbose_name = ('Forests'), help_text = "")
    asport = models.CharField('App Server Port Number', max_length = 10, help_text = "")
    
    def __str__(self):
        return (self.name)
        
class JSONstore(models.Model):
    """
    Define JSON data storage locations.
    """    

    dbtype = models.CharField('Storage Type', max_length = 25, help_text = "")
    name = models.CharField('Storage Name', max_length = 250, help_text = "")
    host = models.CharField('Host Name', max_length = 500, help_text = "")
    port = models.CharField('Port Number', max_length = 10, help_text = "")
    dbname = models.CharField('Database Name', max_length = 250, help_text = "")
    user = models.CharField('User Name', max_length = 250, help_text = "")
    pw = models.CharField('User Password', max_length = 250, help_text = "")
    hostip = models.CharField('Host IP', max_length = 45, help_text = "")
    forests = models.PositiveSmallIntegerField(verbose_name = ('Forests'), help_text = "")
    asport = models.CharField('App Server Port Number', max_length = 10, help_text = "")
    
    def __str__(self):
        return (self.name)
    
class RDFstore(models.Model):
    """
    Define RDF data storage locations.
    """

    dbtype = models.CharField('Storage Type', max_length = 25, help_text = "")
    name = models.CharField('Storage Name', max_length = 250, help_text = "")
    host = models.CharField('Host Name', max_length = 500, help_text = "")
    port = models.CharField('Port Number', max_length = 10, help_text = "")
    dbname = models.CharField('Database Name', max_length = 250, help_text = "")
    user = models.CharField('User Name', max_length = 250, help_text = "")
    pw = models.CharField('User Password', max_length = 250, help_text = "")
    hostip = models.CharField('Host IP', max_length = 45, help_text = "")
    forests = models.PositiveSmallIntegerField(verbose_name = ('Forests'), help_text = "")
    asport = models.CharField('App Server Port Number', max_length = 10, help_text = "")

    def __str__(self):
        return (self.name)
    
class Datamodel(models.Model):
    """
    The Datamodel model provides a location to store the model information and metadata 
    about the model.


    [NAMESPACES]
    any additional namespaces must be defined with their abbreviations.
    {abbrev}:{namespace URI}
    Example:  dul: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#

    """

    project = models.CharField('Project', max_length = 50, help_text = "")
    title = models.CharField('Title', max_length = 250, help_text = "")
    description = models.TextField(verbose_name = ('Description'), help_text = "")
    copyright = models.CharField('Copyright', max_length = 250, help_text = "")
    author = models.CharField('Author', max_length = 250, help_text = "")
    definition_url = models.CharField('Defining URL', max_length = 500, help_text = "")
    namespaces = models.TextField(verbose_name = ('Additional Namespaces'), help_text = "")
    xml_store = models.ForeignKey(XMLstore, on_delete=models.CASCADE)
    rdf_store = models.ForeignKey(RDFstore, on_delete=models.CASCADE)
    json_store = models.ForeignKey(JSONstore, on_delete=models.CASCADE)
    dmid = models.CharField('Data Model ID', max_length = 40, help_text = "")
    dataid = models.CharField('Data Cluster ID', max_length = 40, help_text = "")
    schema = models.TextField(verbose_name = ('XML Schema'), help_text = "")
    rdf = models.TextField(verbose_name = ('RDF'), help_text = "")

    def __str__(self):
        return (self.title)
    
class Component(models.Model):
    """
    The Component model provides a location to store the datatype and metadata information about each column in the CSV.
    """

    header = models.CharField('CSV Column Header', max_length = 100, help_text = "")
    label = models.CharField('Label Value', max_length = 250, help_text = "")
    datatype = models.CharField('Datatype', max_length = 10, help_text = "")
    min_len = models.PositiveSmallIntegerField(verbose_name = ('Minimum Length'), help_text = "")
    max_len = models.PositiveSmallIntegerField(verbose_name = ('Maximum Length'), help_text = "")
    choices = models.TextField(verbose_name = ('String Enumerations'), help_text = "")
    regex = models.CharField('Regular Expression', max_length = 100, help_text = "")
    min_incl = models.CharField('Minimum Value (Inclusive)', max_length = 100, help_text = "")
    max_incl = models.CharField('Maximum Value (Inclusive)', max_length = 100, help_text = "")
    min_excl = models.CharField('Minimum Value (Exclusive)', max_length = 100, help_text = "")
    max_excl = models.CharField('Maximum Value (Exclusive)', max_length = 100, help_text = "")
    description = models.TextField(verbose_name = ('Description'), help_text = "")
    definition_url = models.CharField('Defining URL', max_length = 500, help_text = "")
    pred_obj = models.TextField(verbose_name = ('List of predicate/object pairs'), help_text = "")
    def_text = models.CharField('Default Text', max_length = 500, help_text = "")
    def_num = models.CharField('Default Number', max_length = 100, help_text = "")
    units = models.CharField('Units', max_length = 50, help_text = "")
    mcid = models.CharField('Component ID', max_length = 40, help_text = "")
    adid = models.CharField('Adapter ID', max_length = 40, help_text = "")
    model_link = models.ForeignKey(Datamodel, on_delete=models.CASCADE)

    def __str__(self):
        return (self.header)

class Validation(models.Model):
    """
    A validation log is created each time data is generated.
    The log column is a CSV file:
    """

    model_id = models.ForeignKey(Datamodel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name = ('Time Stamp'), auto_now_add=True, help_text = "")
    log =  models.TextField(verbose_name = ('CSV Log'), help_text = "")
    
    def __str__(self):
        return (self.timestamp)
    