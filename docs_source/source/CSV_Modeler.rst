===========
CSV Modeler
===========

Introduction
============

The **CSV Modeler** application allows importing of a CSV file and creating a complete data model with semantics and validation for the imported file. This can be used in a pipeline where CSV files are regularly generated and should adhere to a well-defined structure with consistent semantics. 

Purpose
=======

**CSV Modeler** is a tool to translate simple CSV formatted data files into computable, semantically enhanced knowledge representations. As a foundation for **crowdsourced**, *automated knowledge base construction*; it provides a path for existing data sets to be used in conjunction with the emerging *graph data, model first* approach in analysis, general artificial intelligence (AGI), and decision support systems. This approach opens the door for the change to a more data-centric approach as opposed to the current application-centric approach. This new path enables automatic, machine processable interoperability avoiding the data quality issues created through data migration, data cleaning and data massaging.

The importance of how this simplifies query and analysis capabilities and improves data quality is discussed in foundational `S3Model <https://s3model.com>`_ documentation and references. However, detailed understanding of S3Model is not required to understand and use the power of this tool.

Target Audience
---------------

Design philosophy is based on the ability for *domain experts* from any field, with very little programming ability to quickly annotate data extracts to improve the usability of the data. Data engineers and data scientists can also benefit from the tool in the same ways as domain experts.

The resulting model can be used in a pipeline to take any existing CSV data sources and create valid XML, JSON documents and RDF triples, that do not lose the context of the source batch/document and adds specific semantics as selected (one time) by the domain expert.

.. image:: _static/pipeline.png
    :width: 600px
    :align: center
    :height: 400px
    :alt: Pipeline

The above diagram shows how data extracts can be converted to rich semantic data. You may or may not need an OpenRefine macro to clean the data. Once a model is defined these consistent CSV files are pipelined through to create one or more of the serializations of the data including all of the semantics defined by the domain expert.

