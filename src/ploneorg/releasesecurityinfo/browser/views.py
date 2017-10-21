# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('ploneorg.releasesecurityinfo')


class ReleaseFolderView(BrowserView):

    pass
