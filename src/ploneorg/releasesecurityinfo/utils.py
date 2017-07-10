# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from httplib2 import ServerNotFoundError
from launchpadlib.launchpad import Launchpad
# from pkg_resources import parse_version
from plone import api

import logging


log = logging.getLogger("ploneorg.releasesecurityinfo")


def update_releasefolder(context):
    try:
        launchpad = Launchpad.login_anonymously('plone release crawler',
                                                'production',
                                                version='devel')
        project = launchpad.load(context.project_name)
        series = project.series

        existing_series = api.content.find(context=context,
                                           depth=1,
                                           portal_type='ReleaseSeries')
        existing_series = {elem.id: elem.getObject() for elem in existing_series}  # NOQA: E501

        existing_releases = api.content.find(context=context,
                                             depth=2,
                                             portal_type='Release')
        existing_releases = {elem.id: elem.getObject() for elem in existing_releases}  # NOQA: E501

        for serie in series:
            name = serie.name
            series_obj = None
            if name not in existing_series.keys():
                log.info('Create new ReleaseSeries for %s', name)
                series_obj = api.content.create(container=context,
                                                type='ReleaseSeries',
                                                id=name,
                                                title=name)
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
                        release_obj = api.content.create(container=series_obj,
                                                         type='Release',
                                                         id=elem.name,
                                                         title=elem.name)
                    else:
                        path = context.absolute_url() + '/' + name + '/' + elem.name  # NOQA: E501
                        release_obj = api.content.get(path=path)
                        log.info('Update Release Information for %s', elem.name)  # NOQA: E501

                    if release_obj is not None:
                        release_obj.code_name = elem.code_name
                        release_obj.active = elem.is_active

                        release_elem = elem.release
                        release_obj.releasedate = release_elem.date_released

                        for f in release_elem.files:
                            log.info(f)
                            # link = f.self_link

    except ServerNotFoundError:
        log.error("Connection Error")
