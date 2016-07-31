# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ploneorg.releasesecurityinfo


class PloneorgReleasesecurityinfoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=ploneorg.releasesecurityinfo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ploneorg.releasesecurityinfo:default')


PLONEORG_RELEASESECURITYINFO_FIXTURE = PloneorgReleasesecurityinfoLayer()


PLONEORG_RELEASESECURITYINFO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEORG_RELEASESECURITYINFO_FIXTURE,),
    name='PloneorgReleasesecurityinfoLayer:IntegrationTesting'
)


PLONEORG_RELEASESECURITYINFO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEORG_RELEASESECURITYINFO_FIXTURE,),
    name='PloneorgReleasesecurityinfoLayer:FunctionalTesting'
)


PLONEORG_RELEASESECURITYINFO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONEORG_RELEASESECURITYINFO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PloneorgReleasesecurityinfoLayer:AcceptanceTesting'
)
