# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from math import fabs
from plone import api
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from ploneorg.releasesecurityinfo.interfaces import IHotfix
from ploneorg.releasesecurityinfo.interfaces import IHotfixFolder
from ploneorg.releasesecurityinfo.interfaces import INameFromReleaseDate
from ploneorg.releasesecurityinfo.interfaces import IRelease
from ploneorg.releasesecurityinfo.interfaces import IReleaseFolder
from ploneorg.releasesecurityinfo.interfaces import IReleaseSeries
from ploneorg.releasesecurityinfo.interfaces import IVulnerability
from ploneorg.releasesecurityinfo.vocabularies import AccessVectorVocabulary
from ploneorg.releasesecurityinfo.vocabularies import AuthenticationVocabulary
from ploneorg.releasesecurityinfo.vocabularies import ComplexityVocabulary
from ploneorg.releasesecurityinfo.vocabularies import ImpactVocabulary
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer

import pkg_resources


@implementer(IReleaseFolder)
class ReleaseFolder(Container):
    pass


@implementer(IReleaseSeries)
class ReleaseSeries(Container):
    pass


@implementer(IRelease)
class Release(Item):
    pass


@implementer(IHotfixFolder)
class HotfixFolder(Container):
    pass


@implementer(INameFromReleaseDate)
class NameFromReleaseDate(object):

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        # Hotfixes have their ID generated from their release date.
        return self.context.release_date.strftime('%Y%m%d')


@implementer(IHotfix)
class Hotfix(Container):

    @property
    def title(self):
        # Hotfixes have their ID generated from their release date.
        return self.release_date.strftime('%Y%m%d')

    def released(self):
        workflowTool = api.portal.get_tool('portal_workflow')
        status = workflowTool.getStatusOf('hotfix_workflow', self)
        state = status['review_state']
        return state

    def setTitle(self, title):
        # Don't allow anything to change the title. While a little
        # crude, this prevents the rename page from setting a title
        # on a hotfix which it's not possible to remove
        return

    def getAffectedVersions(self):
        """ Pull affected versions from the contained vulnerabilities."""

        brains = api.content.find(
            object_provides=IVulnerability.__identifier__,
            path={'query': '/'.join(self.getPhysicalPath())},
        )

        result = []
        for brain in brains:
            result.extend(brain.getObject().affected_versions)

        result = sorted(set(result), key=pkg_resources.parse_version)
        result.reverse()

        return result


@implementer(IVulnerability)
class Vulnerability(Item):

    @property
    def cvss_score(self):
        """ Scoring, based on http://www.first.org/cvss/cvss-guide#i2.4
        """

        scoring = ['low', 'medium', 'high']
        impact_scoring = [0.0, 0.275, 0.660]
        authentication_scoring = [0.45, 0.56, 0.704]
        complexity_scoring = [0.35, 0.61, 0.71]
        vector_scoring = [0.395, 0.646, 1.0]

        access_vector = vector_scoring[scoring.index(
            AccessVectorVocabulary.getTerm(self.cvss_access_vector).token)]
        access_complexity = complexity_scoring[scoring.index(
            ComplexityVocabulary.getTerm(self.cvss_access_complexity).token)]
        authentication = authentication_scoring[scoring.index(
            AuthenticationVocabulary.getTerm(self.cvss_authentication).token)]
        conf_impact = impact_scoring[scoring.index(
            ImpactVocabulary.getTerm(self.cvss_confidentiality_impact).token)]
        integ_impact = impact_scoring[scoring.index(
            ImpactVocabulary.getTerm(self.cvss_integrity_impact).token)]
        avail_impact = impact_scoring[scoring.index(
            ImpactVocabulary.getTerm(self.cvss_availability_impact).token)]

        impact = 10.41 * (1 - (1 - conf_impact) * (1 - integ_impact) *
                              (1 - avail_impact))
        exploitability = (20 * access_vector * access_complexity *
                          authentication)

        if impact == 0:
            f_impact = 0
        else:
            f_impact = 1.176

        base_score = round(fabs(((0.6 * impact) +
                                (0.4 * exploitability) - 1.5) * f_impact), 1)

        return base_score
