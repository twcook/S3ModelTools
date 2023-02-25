"""
Test that the S3MPython config file is correctly found and .
"""

import os
import configparser
from pathlib import Path
from unittest import TestCase
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent.parent

class TestWorkingDir(TestCase):
    """
    Test that the working directory is set correctly and the S3MPython configuration is found.
    """

    def test_working_dir(self):
        """
        Test that the working directory is set correctly.
        """
        self.assertTrue(os.path.isfile(os.path.join(BASE_DIR,'../conf', 'S3MPython.conf')))

    def test_xml_catalog(self):
        """
        Test that the XML catalog is set correctly.
        """
        if os.path.isfile(os.path.join(BASE_DIR,'../conf', 'S3MPython.conf')):
            config = configparser.ConfigParser()
            config.read(os.path.join(BASE_DIR,'../conf', 'S3MPython.conf'))
            cat_dir = config['S3MPython']['catalog']
            cat_file = os.path.join(cat_dir, 'catalog.xml')
            self.assertTrue(os.path.isfile(cat_file))
        else:
            print(f'No S3MPython configuration file found.\n\n')
            exit()

    def test_rm_schema_location(self):
        """
        Test that the XML Schema RM is set correctly.
        """
        if os.path.isfile(os.path.join(BASE_DIR,'../conf', 'S3MPython.conf')):
            config = configparser.ConfigParser()
            config.read(os.path.join(BASE_DIR,'../conf', 'S3MPython.conf'))
            cat_dir = config['S3MPython']['catalog']
            cat_file = os.path.join(cat_dir, 'catalog.xml')
        else:
            print(f'No S3MPython configuration file found.\n\n')
        
        with open(cat_file, 'rb') as f:
            xml = f.read()
        root = etree.fromstring(xml)
        rm_schema_file = root[1].attrib['uri']
        self.assertTrue(os.path.isfile(rm_schema_file))

     
