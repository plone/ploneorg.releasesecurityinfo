# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from ploneorg.releasesecurityinfo.testing import PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING  # noqa
from ploneorg.releasesecurityinfo.interfaces import IPloneRelease

import unittest2 as unittest


class PloneReleaseIntegrationTest(unittest.TestCase):

    layer = PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='PloneRelease')
        schema = fti.lookupSchema()
        self.assertEqual(IPloneRelease, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='PloneRelease')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='PloneRelease')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IPloneRelease.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('PloneRelease', 'PloneRelease')
        self.assertTrue(
            IPloneRelease.providedBy(self.portal['PloneRelease'])
        )
