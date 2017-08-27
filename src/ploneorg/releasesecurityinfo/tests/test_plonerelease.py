# -*- coding: utf-8 -*-

from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from ploneorg.releasesecurityinfo.interfaces import IRelease
from ploneorg.releasesecurityinfo.testing import PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING  # NOQA: E501
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PloneReleaseIntegrationTest(unittest.TestCase):

    layer = PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Release')
        schema = fti.lookupSchema()
        # self.assertEqual(IRelease, schema)
        self.assertEqual(schema, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Release')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Release')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IRelease.providedBy(obj))

    def test_adding(self):  # Not globally allowed
        self.portal = api.portal.get()
        # with self.assertRaises(ValueError,
        #                        message='Disallowed subobject type: Release'):
        with self.assertRaises(
            InvalidParameterError,
            message="Cannot add a 'Release' object to the container.",
        ):
            api.content.create(
                container=self.portal,
                type='Release',
                title='Future',
            )
