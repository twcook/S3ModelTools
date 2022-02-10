.. _setup:

===========
Tools Setup
===========

* Install the prerequisites.
* Edit the configuration file (if desired)


Prerequisites
=============

* Download the `latest release <https://github.com/twcook/S3ModelTools>`_


Configuration
=============

.. _config:

.. warning::

    Only edit the configuration file with a text editor. Do not use a word processing application such as MS Word or LibreOffice. There are many great opensource and free text editors from which to choose.  Some favorites, in no particular order, are:

    - `Atom <https://atom.io/>`_
    - `VS Code <https://code.visualstudio.com/>`_
    - `Sublime <https://www.sublimetext.com/>`_

The initial S3ModelTools.conf file should be okay for most uses and indeed for the initial tutorial. You are encouraged to make backup copies, under different names, of the configuration file for different use cases/projects. The active configuration, however, is always the one named **S3ModelTools.conf**. 

Config File Details
===================
Here we cover the details of the configuration options.


.. sourcecode:: text

    ; The default data (CSV) file delimiter is defined here.
    ; allowed delimiter (field separator) types are one of these:  , ; : | $
    ; A different delimiter may be passed on the commandline that will override this one.
    delim: ,


**There are no options editable by the user in the SYSTEM section.**

.. sourcecode:: text


    [SYSTEM]
    version: 1.0.0
    rmversion: 3.1.0

The *version* is the current version of S3ModelTools.
The *rmversion* is the version of the S3Model Reference Model that is used for generated data models.

