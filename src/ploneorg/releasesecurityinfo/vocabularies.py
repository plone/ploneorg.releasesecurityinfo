# -*- coding: utf-8 -*-

from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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


@provider(IVocabularyFactory)
def ImpactVocabulary(context):
    return SimpleVocabulary([
        SimpleTerm('N', 'low', title='None'),
        SimpleTerm('P', 'medium', title='Partial'),
        SimpleTerm('C', 'high', title='Complete'),
    ])


@provider(IVocabularyFactory)
def ComplexityVocabulary(context):
    return SimpleVocabulary([
        SimpleTerm('H', 'low', 'High'),
        SimpleTerm('M', 'medium', 'Medium'),
        SimpleTerm('L', 'high', 'Low')
    ])


@provider(IVocabularyFactory)
def AccessVectorVocabulary(context):
    return SimpleVocabulary([
        SimpleTerm('L', 'low', 'Local'),
        SimpleTerm('A', 'medium', 'Adjacent Network'),
        SimpleTerm('N', 'high', 'Network')
    ])


@provider(IVocabularyFactory)
def AuthenticationVocabulary(context):
    return SimpleVocabulary([
        SimpleTerm('M', 'low', 'Multiple'),
        SimpleTerm('S', 'medium', 'Single'),
        SimpleTerm('N', 'high', 'None')
    ])


@provider(IVocabularyFactory)
def plone_version_vocabulary(context):
    terms = []
    if context:
        pass
#       versions = context.release
#       for version in versions:
#            terms.append(SimpleVocabulary.createTerm(version['name']))
    return SimpleVocabulary(terms)
