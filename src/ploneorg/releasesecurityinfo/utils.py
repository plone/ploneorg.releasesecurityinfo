# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from DateTime import DateTime
from httplib2 import ServerNotFoundError
from launchpadlib.launchpad import Launchpad
# from pkg_resources import parse_version
from plone import api
from ploneorg.releasesecurityinfo.contents import ReleaseFolder
from ploneorg.releasesecurityinfo.contents import ReleaseSeries
from Products.CMFPlone.Portal import PloneSite
from z3c.formwidget.optgroup.widget import OptgroupTerm
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import logging


log = logging.getLogger('ploneorg.releasesecurityinfo')


def update_releasefolder(context):
    try:
        launchpad = Launchpad.login_anonymously(
            'plone release crawler',
            'production',
            version='devel',
        )
        project = launchpad.load(context.project_name)
        series = project.series

        existing_series = api.content.find(
            context=context,
            depth=1,
            portal_type='ReleaseSeries',
        )
        existing_series = {elem.id: elem.getObject() for elem in existing_series}  # NOQA: E501

        existing_releases = api.content.find(
            context=context,
            depth=2,
            portal_type='Release',
        )
        existing_releases = {elem.id: elem.getObject() for elem in existing_releases}  # NOQA: E501

        for serie in series:
            name = serie.name
            series_obj = None
            if name not in existing_series.keys():
                log.info('Create new ReleaseSeries for %s', name)
                series_obj = api.content.create(
                    container=context,
                    type='ReleaseSeries',
                    id=name,
                    title=name,
                )
            else:
                path = context.absolute_url() + '/' + name
                series_obj = api.content.get(path=path)
                series_obj = existing_series.get(name)
                log.info('Update ReleaseSeries Information for %s', name)

            if series_obj is not None:
                series_obj.title = name
                series_obj.description = serie.summary
                series_obj.status = serie.status
                # series_obj.is_development_focus = serie.is_development_focus
                series_obj.branch = serie.branch
                series_obj.url_pattern = serie.release_finder_url_pattern

                series_obj.release_manager = serie.owner.display_name

                release_obj = None
                for elem in serie.all_milestones:
                    if elem.name not in existing_releases.keys():
                        log.info('Create new Release for %s', elem.name)
                        release_obj = api.content.create(
                            container=series_obj,
                            type='Release',
                            id=elem.name,
                            title=elem.name,
                        )
                    else:
                        path = context.absolute_url() + '/' + name + '/' + elem.name  # NOQA: E501
                        release_obj = api.content.get(path=path)
                        log.info('Update Release Information for %s', elem.name)  # NOQA: E501

                    if release_obj is not None:
                        release_obj.code_name = elem.code_name
                        release_obj.active = elem.is_active
                        release_obj.releasedate = DateTime(elem.release.date_released)  # NOQA: E501

                        for f in elem.release.files:
                            log.info(f)
                            # link = f.self_link

    except ServerNotFoundError:
        log.error('Connection Error')


@provider(IVocabularyFactory, IContextSourceBinder)
def version_vocabulary(context):
    parent = context.aq_parent
    while not isinstance(parent, ReleaseFolder):
        if isinstance(parent, PloneSite):
            return SimpleVocabulary([])
        parent = parent.aq_parent
    versions = []
    if isinstance(parent, ReleaseFolder):
        for name, obj in parent.items():
            if isinstance(obj, ReleaseSeries):
                series = obj
                for release_title, release in series.items():
                    versions.append(OptgroupTerm(
                        value=release_title,
                        token=str(release_title),
                        title=release_title,
                        optgroup=series.title,
                    ))
    return SimpleVocabulary(versions)
