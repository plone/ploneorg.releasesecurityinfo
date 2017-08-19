# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from ploneorg.releasesecurityinfo.interfaces import IHotfix
from ploneorg.releasesecurityinfo.utils import update_releasefolder
from Products.Five.browser import BrowserView
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
        brains = api.content.find(object_provides=IHotfix.__identifier__)

        return sorted(brains, key=lambda hotfix: hotfix.id, reverse=True)

    def get_versions(self):
        versions = []

        """
        releaseseries = api.content.find(portal_type='ReleaseSeries')
        for brain in releaseseries:
            series = brain.getObject()
            print series.title
            versions.append(series)
        """

        releases = api.content.find(portal_type='Release')
        for brain in releases:
            release = brain.getObject()
            versions.append(release)

        security = []
        security_brains = api.content.find(
            portal_type='ReleaseSeries',
            is_security_supported=True,
        )
        for brain in security_brains:
            series = brain.getObject()
            security.append(series.title)

        maintenance = []
        maintenance_brains = api.content.find(
            portal_type='ReleaseSeries',
            is_active_maintained=True,
        )
        for brain in maintenance_brains:
            series = brain.getObject()
            maintenance.append(series.title)

        result = []
        for v in sorted(versions, reverse=True):
            version = v.title
            data = {
                'name': version,
                'date': v.releasedate,
                'security': version in security,
                'maintenance': version in maintenance,
            }
            result.append(data)
        return result

    def get_hotfixes_for_version(self, version):
        # get all hotfixes
        result = []
        brains = api.content.find(object_provides=IHotfix.__identifier__)

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
        versions = []
        """
        releaseseries = api.content.find(portal_type='ReleaseSeries')
        for brain in releaseseries:
            series = brain.getObject()
            print series.title
            versions.append(series)
        """
        releases = api.content.find(portal_type='Release')
        for brain in releases:
            release = brain.getObject()
            print release.title
            versions.append(release)

        security = []
        security_brains = api.content.find(
            portal_type='ReleaseSeries',
            is_security_supported=True,
        )
        for brain in security_brains:
            series = brain.getObject()
            security.append(series.title)

        maintenance = []
        maintenance_brains = api.content.find(
            portal_type='ReleaseSeries',
            is_active_maintained=True,
        )
        for brain in maintenance_brains:
            series = brain.getObject()
            maintenance.append(series.title)

        result = []

        for v in sorted(versions, reverse=True):
            version = v.title
            date_format = '%b %d, %Y'
            version_release_date = datetime.strptime(
                v.releasedate, date_format).date()

            vdata = {
                'name': version,
                'date': version_release_date.isoformat(),
                'security': version in security,
                'maintenance': version in maintenance,
                'hotfixes': {

                },
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
