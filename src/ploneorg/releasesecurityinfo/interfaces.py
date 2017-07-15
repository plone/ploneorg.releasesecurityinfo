# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.app.content.interfaces import INameFromTitle
from ploneorg.releasesecurityinfo import _
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPloneOrgReleaseSecurityInfoLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IReleaseFolder(model.Schema):
    """
    Schema for ReleaseFolder.
    """
    model.load("models/releasefolder.xml")


class IReleaseSeries(model.Schema):
    """
    Schema for ReleaseSeries.
    """
    model.load("models/releaseseries.xml")


class IRelease(model.Schema):
    """
    Schema for Release.
    """
    model.load("models/release.xml")


class IHotfixFolder(model.Schema):
    """
    Schema for HotfixFolder.
    """
    model.load("models/hotfixfolder.xml")


class IHotfix(model.Schema):
    """
    Schema for Hotfix.
    """
    model.load("models/hotfix.xml")


class IVulnerability(model.Schema):
    """
    Schema for Vulnerability.
    """
    model.load("models/vulnerability.xml")


class INameFromReleaseDate(INameFromTitle):
    def title():
        """Return a processed title"""