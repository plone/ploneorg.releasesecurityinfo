# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPloneOrgReleaseSecurityInfoLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IReleaseFolder(model.Schema):
    """
    Schema for ReleaseFolder.
    """


class IReleaseSeries(model.Schema):
    """
    Schema for ReleaseSeries.
    """


class IRelease(model.Schema):
    """
    Schema for Release.
    """


class IHotfixFolder(model.Schema):
    """
    Schema for HotfixFolder.
    """


class IHotfix(model.Schema):
    """
    Schema for Hotfix.
    """


class IVulnerability(model.Schema):
    """
    Schema for Vulnerability.
    """
