# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from datetime import datetime
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from ploneorg.releasesecurityinfo.interfaces import IHotfix
from ploneorg.releasesecurityinfo.utils import update_releasefolder
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides

import json


class ReleaseFolderUpdateView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        update_releasefolder(self.context)
        self.request.response.redirect(self.context.absolute_url())


class HotfixFeed(BrowserView):
    """ Load the collection of hotfixes and perform any processing required to
    present the correct feed to the client
    """

    pass


class HotfixListing(BrowserView):
    """ Load the collection of hotfixes and perform any processing required to
    present the correct list to the client
    """

    def get_hotfixes(self):
        context = aq_inner(self.context)
        tools = getMultiAdapter((context, self.request), name=u'plone_tools')

        portal_catalog = tools.catalog()
        brains = portal_catalog(object_provides=IHotfix.__identifier__)

        return sorted(brains, key=lambda hotfix: hotfix.id, reverse=True)

    def get_versions(self):
        registry = getUtility(IRegistry)
        versions = registry['plone.versions']
        security = registry['plone.securitysupport']
        maintenance = registry['plone.activemaintenance']
        result = []
        for v in sorted(versions, reverse=True):
            version = v.split('-')[0]
            data = {
                'name': version,
                'date': v.split('-')[1],
                'security': version in security,
                'maintenance': version in maintenance
            }
            result.append(data)
        return result

    def get_hotfixes_for_version(self, version):
        # get all hotfixes
        result = []
        context = aq_inner(self.context)
        tools = getMultiAdapter((context, self.request), name=u'plone_tools')

        portal_catalog = tools.catalog()
        brains = portal_catalog(object_provides=IHotfix.__identifier__)

        for brain in brains:
            if version in brain.getObject().getAffectedVersions():
                result.append(brain)

        return sorted(result, key=lambda hotfix: hotfix.id, reverse=True)


class HotfixJSONListing(HotfixListing):
    """ Load the collection of hotfixes and perform any processing required to
    present the correct list to the client via json
    """

    def __init__(self, context, request):
        super(HotfixJSONListing, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        registry = getUtility(IRegistry)
        versions = registry['plone.versions']
        security = registry['plone.securitysupport']
        maintenance = registry['plone.activemaintenance']
        result = []

        for v in sorted(versions, reverse=True):
            version = v.split('-')[0]
            date_format = '%b %d, %Y'
            plone_version_release_date = datetime.strptime(
                v.split('-')[1], date_format).date()

            vdata = {
                'name': version,
                'date': plone_version_release_date.isoformat(),
                'security': version in security,
                'maintenance': version in maintenance,
                'hotfixes': {

                }
            }

            applied_hotfixes = []
            fixs = self.get_hotfixes_for_version(version)
            for f in fixs:
                fix = f.getObject()
                fix_data = {
                    'name': fix.id,
                    'url': fix.absolute_url(),
                    'release_date': fix.release_date.isoformat(),
                }
                if fix.hotfix is not None:
                    fix_data['download_url'] = fix.absolute_url() + \
                        '/@@download/hotfix'
                    fix_data['md5'] = fix.hotfix.md5
                    fix_data['sha1'] = fix.hotfix.sha1
                    fix_data['pypi_name'] = 'Products.PloneHotfix' + fix.id

                applied_hotfixes.append(fix_data)
            vdata['hotfixes'] = applied_hotfixes
            result.append(vdata)

        self.request.RESPONSE.setHeader('Content-Type',
                                        'application/json; charset="UTF-8"')

        if 'version' in self.request.form:
            requested_version = self.request.form['version']
            for r in result:
                if r['name'] == requested_version:
                    result = r
                    break
            else:
                result = None

        self.request.response.setBody(json.dumps(result))
        return self.request.response
