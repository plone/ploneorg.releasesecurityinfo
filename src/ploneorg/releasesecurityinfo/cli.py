from ploneorg.releasesecurityinfo.utils import update_releasefolder

import argparse
import logging


logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('ploneorg.releasesecurityinfo-cli')

"""
usage:
bin/instance -O <portal_id> update_releasefolder
                                  <Path to releasefolder relative to Zope root>
"""


def cli_update(app, args):
    parser = argparse.ArgumentParser('updates the releasefolder')
    parser.add_argument('-c')
    parser.add_argument(
        'context',
        help='Path to ReleaseFolder relative to Zope root.\
              Ex:Plone/<ReleaseFolder name>'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        default=False,
        help='print more verbose output',
        action='store_true'
    )
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.INFO)
    folder = app.unrestrictedTraverse(args.context)
    update_releasefolder(folder, logger=log)
