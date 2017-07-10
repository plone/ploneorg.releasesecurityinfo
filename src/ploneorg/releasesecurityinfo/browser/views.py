# -*- coding: utf-8 -*-

from plone.protect.interfaces import IDisableCSRFProtection
from ploneorg.releasesecurityinfo.utils import update_releasefolder
from Products.Five.browser import BrowserView
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides


class ReleaseFolderUpdateView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        update_releasefolder(self.context)
        self.request.response.redirect(self.context.absolute_url())
