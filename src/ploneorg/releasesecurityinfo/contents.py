# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.dexterity.content import Container
from plone.dexterity.content import Item
from ploneorg.releasesecurityinfo.interfaces import IHotfix
from ploneorg.releasesecurityinfo.interfaces import IHotfixFolder
from ploneorg.releasesecurityinfo.interfaces import IRelease
from ploneorg.releasesecurityinfo.interfaces import IReleaseFolder
from ploneorg.releasesecurityinfo.interfaces import IReleaseSeries
from ploneorg.releasesecurityinfo.interfaces import IVulnerability
from zope.interface import implementer
from zope.interface import implements


@implementer(IReleaseFolder)
class ReleaseFolder(Container):
    implements(IReleaseFolder)


@implementer(IReleaseSeries)
class ReleaseSeries(Container):
    implements(IReleaseSeries)


@implementer(IRelease)
class Release(Item):
    implements(IRelease)


@implementer(IHotfixFolder)
class HotfixFolder(Container):
    implements(IHotfixFolder)


@implementer(IHotfix)
class Hotfix(Container):
    implements(IHotfix)


@implementer(IVulnerability)
class Vulnerability(Item):
    implements(IVulnerability)
