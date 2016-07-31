# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from ploneorg.releasesecurityinfo.testing import PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that ploneorg.releasesecurityinfo is properly installed."""

    layer = PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ploneorg.releasesecurityinfo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ploneorg.releasesecurityinfo'))

    def test_browserlayer(self):
        """Test that IPloneorgReleasesecurityinfoLayer is registered."""
        from ploneorg.releasesecurityinfo.interfaces import (
            IPloneorgReleasesecurityinfoLayer)
        from plone.browserlayer import utils
        self.assertIn(IPloneorgReleasesecurityinfoLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['ploneorg.releasesecurityinfo'])

    def test_product_uninstalled(self):
        """Test if ploneorg.releasesecurityinfo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ploneorg.releasesecurityinfo'))

    def test_browserlayer_removed(self):
        """Test that IPloneorgReleasesecurityinfoLayer is removed."""
        from ploneorg.releasesecurityinfo.interfaces import IPloneorgReleasesecurityinfoLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPloneorgReleasesecurityinfoLayer, utils.registered_layers())
