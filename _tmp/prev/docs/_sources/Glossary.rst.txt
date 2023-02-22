========
Glossary
========

while many terms have more than one definition. The definitions presented here are in the context of managing data, especially in the S3Model context.


.. _ai:

An area of computer science that deals with giving machines the ability to seem like they have human intelligence. Also, the power of a machine to copy intelligent human behavior.

.. _compliance:

**Compliance** is the practice of following regulations set forth by corporate governance, industry organizations, and governments. These regulations set forth protocols for how sensitive data is collected, used, stored, and managed, among other requirements.

.. _computable-models:

**Computable models** in this context, are data models that can be used to validate data and insure data compliance based on the structure and rules contained within the data model.

.. _constraints:

A **constraint** is simply *a limitation or restriction.* In the context of S3Model, constraints are mapped to the XML Schema constraint model. These constraints are sometimes referred to as `restrictions or facets <https://www.w3schools.com/xml/schema_facets.asp>`_.

.. _contextual:

**Contextual** - Contextual means to view information as a whole- both the facts and where they came from.

.. _DM:

**DM** short for Data Model in S3Model is defined as a set of constraints on the Reference Model. In the reference implementation this will be an XML Schema that imports the Refernce Model schema. In Python it is a Python file that imports the Python Reference Model.

.. _DM-ID:

The **DM-ID** is a unique identifier for each and every data model created in the S3Model ecosystem. No identifier can be duplicated because of the construction method. All identifiers in S3Model use a Collision Resistant Unique Identifier `(CUID) <https://github.com/ericelliott/cuid>`_. Thouogh there are ports to virtually all programming languages, you can also get them `online here <https://www.getuniqueid.com/cuid>`_.

.. _data-instance:

A **Data Instance** is specific file or database entry that contains information based on some model. Examples include; an XML file, a JSON file, a row and its relations in a SQL database, a text file from an editor, or other concrete entity. 

.. _data-modeling:

**Data Modeling** - A data model (or datamodel) is an abstract model that organizes elements of data and standardizes how they relate to one another and to the properties of real-world entities. 

.. _data-analyst:

**Data analysts** use machine learning and AI tools to answer business questions.

.. _data-scientists:

**Data scientists** typically spend more time modeling data and building analytic tools.

.. _domain-experts:

**Domain expert** - A domain expert is a person with special knowledge or skills in a particular area of endeavor. An accountant is an expert in the domain of accountancy, for example. The development of accounting software requires knowledge in two different domains, namely accounting and software.

.. _esperanto:

**Esperanto** - an artificial language devised in 1887 as an international medium of communication, based on roots from the chief European languages. Majority of the speakers are found in the United Kingdom, Belgium, Brazil, United States, Poland, Italy, Germany and France. Surprisingly, there are also many Esperanto speakers in China and Japan. Dr. Zamenhof created the language to fight nationalism and boost internationalism and mutual understanding.

.. _graphdb:

A **graph database** stores nodes and relationships instead of tables, or documents. Data is stored just like you might sketch ideas on a whiteboard. Your data is stored without restricting it to a pre-defined model, allowing a very flexible way of thinking about and using it. It must be noted that not having a pre-defined model has many drawbacks, lack of data validation being a major one. S3Model provides a mechanism to have a strong model and still store your data as a knowledge graph. 

.. _json:

**JavaScript Object Notation (JSON)** is a standard text-based format for representing structured data based on JavaScript object syntax. It is commonly used for transmitting data in web applications (e.g., sending some data from the server to the client, so it can be displayed on a web page, or vice versa).

.. _model-components:

**Model Components** are defined as XML Schema `complexTypes <https://www.w3schools.com/xml/el_complextype.asp>`_ in the reference implementation. 

.. _ontologies:

**Ontologies** - a set of concepts and categories in a subject area or domain that shows their properties and the relations between them. One major advantage of using a domain ontology is its ability to define a semantic model of the data combined with the associated domain knowledge. Ontologies can also be used to define links between different types of semantic knowledge. Thus, ontologies can be used in formulating data analysis strategies.

.. _owl:

**OWL** - The W3C Web Ontology Language (OWL) is a Semantic Web language designed to represent rich and complex knowledge about things, groups of things, and relations between things. 

.. _pred-models:

**Predictive Models** - Predictive modeling is a commonly used statistical technique to predict future behavior. In predictive modeling, data is collected, a statistical model is formulated, predictions are made, and the model is validated (or revised) as additional data becomes available.

.. _rdf:

**RDF** - RDF is a standard model for data interchange on the Web. Although frequently referred to as a *language*, RDF is mainly a data model. It is based on the idea that the things being described have properties, which have values, and that resources can be described by making statements. These statements consist of three components; a subject, a predicate, and an object. It should be noted that RDF is also a vocabulary that along with the RDFS vocabulary provides a set of terms that can be used for creating general/abstract descriptions of resources. OWL is a vocabulary built with RDF and RDFS vocabularies that provide new terms for creating more detailed descriptions of resources.

.. _RM:

A **Reference Model** (RM) is an abstract framework or domain-specific ontology consisting of an interlinked set of clearly defined concepts produced by an expert or body of experts to encourage clear communication.

.. _s3model:

**S3Model** is a modeling approach that includes a comprehensive reference model. Data Models are created by domain experts or other interested individuals that want to model some data. By creating this data model, the creator can be sure that when they send their data to a downstream user, such as an analyst, that user will have all of the computable, contextual information they need to understand the origin and meaning of the data. 

.. _sem-int:

**Semantic Interoperability** - Semantic interoperability denotes the ability of different applications and business partners to understand exchanged data in a similar way, implying a precise and unambiguous meaning of the exchanged information.

.. _sqldb:

**SQL** stands for Structured Query Language. It's used for relational databases. A SQL database is a collection of tables that stores a specific set of structured data.

.. _validation:

**Validation** means checking the accuracy and quality of source data before using, importing or otherwise processing data. Different types of validation can be performed depending on destination constraints or objectives. For example, you could use data validation to make sure a value is a number between 1 and 6, make sure a date occurs in the next 30 days, or make sure a text entry is less than 25 characters.

.. _validation-chain:

A **validation chain** is a series of complimentary components that serve to perform :ref:`validation <validation>`

.. _xml:

**XML** stands for extensible markup language. A markup language is a set of codes, or tags, that describes the text in a digital document. ... XML, a more flexible cousin of HTML, makes it possible to conduct complex business over the Internet.

.. _xmldb:

An XML database is a database that stores data in XML format. This type of database is suited for businesses with data in XML format and for situations where XML storage is a practical way to archive data, metadata and other digital resources.
