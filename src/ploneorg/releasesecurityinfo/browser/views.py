# -*- coding: utf-8 -*-

from pkg_resources import parse_version
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from ploneorg.releasesecurityinfo.contents import ReleaseFolder
from ploneorg.releasesecurityinfo.contents import ReleaseSeries
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

    def get_versions(self, context):
        versions = []
        parent = context.aq_parent
        while not isinstance(parent, ReleaseFolder):
            parent = parent.aq_parent
        if isinstance(parent, ReleaseFolder):
            for name, obj in parent.items():
                if isinstance(obj, ReleaseSeries):
                    series = obj
                    for release_title, release in series.items():
                        releaseinfo = (
                            release,
                            series.is_security_supported,
                            series.is_active_maintained,
                        )
                        versions.append(releaseinfo)
        result = []
        for v in sorted(
            versions,
            key=lambda version: parse_version(version[0].title),
            reverse=True,
        ):
            version = v[0].title
            data = {
                'name': version,
                'date': v[0].releasedate,
                'security': v[1],
                'maintenance': v[2],
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
        parent = self.context.aq_parent
        while not isinstance(parent, ReleaseFolder):
            parent = parent.aq_parent
        if isinstance(parent, ReleaseFolder):
            for name, obj in parent.items():
                if isinstance(obj, ReleaseSeries):
                    series = obj
                    for release_title, release in series.items():
                        releaseinfo = (release, series.is_security_supported,
                                       series.is_active_maintained)
                        versions.append(releaseinfo)
        result = []
        for v in sorted(
            versions,
            key=lambda version: parse_version(version[0].title),
            reverse=True,
        ):
            version = v[0].title
            version_release_date = v[0].releasedate

            vdata = {
                'name': version,
                'date': version_release_date.strftime('%Y-%m-%d'),
                'security': v[1],
                'maintenance': v[2],
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
                    'release_date': fix.release_date.strftime('%Y-%m-%d'),
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
