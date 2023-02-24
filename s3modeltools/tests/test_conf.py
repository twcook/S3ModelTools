"""
Test that the XML catalog is working correctly.
"""

import os
import configparser
from django.test import TestCase
from lxml import etree

class TestWorkingDir(TestCase):
    """
    Test that the working directory is set correctly.
    """

    def test_working_dir(self):
        """
        Test that the working directory is set correctly.
        """
        workdir = os.getcwd()
        print(f'Working directory: {workdir}\n\n')
        self.assertTrue(os.path.isfile(os.path.join(workdir,'../conf', 'S3MPython.conf')))

    def test_xml_catalog(self):
        """
        Test that the XML catalog is set correctly.
        """
        workdir = os.getcwd()
        print(f'Working directory: {workdir}\n\n')
        self.assertTrue(os.path.isfile(os.path.join(workdir,'../conf', 'catalog.xml')))
        