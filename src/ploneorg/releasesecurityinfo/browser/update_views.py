# -*- coding: utf-8 -*-
"""Update Views for ReleaseFolder."""

from plone.protect.interfaces import IDisableCSRFProtection
from ploneorg.releasesecurityinfo.utils import update_releasefolder
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('ploneorg.releasesecurityinfo')


class ReleaseFolderUpdateView(BrowserView):
    """Update View for ReleaseFolder."""

    def __call__(self):
        """Call Method used on actual call of the view."""
        alsoProvides(self.request, IDisableCSRFProtection)
        update_releasefolder(self.context, logger=log)
        self.request.response.redirect(self.context.absolute_url())
