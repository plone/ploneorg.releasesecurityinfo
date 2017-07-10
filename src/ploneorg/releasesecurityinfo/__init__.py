# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


_ = MessageFactory('ploneorg.releasesecurityinfo')


@provider(IVocabularyFactory)
def state_vocabulary(context):
    return SimpleVocabulary([
        SimpleTerm(value=u'EXPERIMENTAL', title=u'Experimental'),
        SimpleTerm(value=u'DEVELOPMENT', title=u'Active Development'),
        SimpleTerm(value=u'FROZEN', title=u'Pre-release Freeze'),
        SimpleTerm(value=u'CURRENT', title=u'Current Stable Release'),
        SimpleTerm(value=u'SUPPORTED', title=u'Supported'),
        SimpleTerm(value=u'OBSOLETE', title=u'Obsolete'),
        SimpleTerm(value=u'FUTURE', title=u'Future'),
    ])
