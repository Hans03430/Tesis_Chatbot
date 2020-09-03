'''
This function contains constants that will be used across the entire library.
'''

import os

ACCEPTED_LANGUAGES = {
    'es': 'es_core_news_sm'
}

LANGUAGES_DICTIONARY_PYPHEN = {
    'es': 'es'
}

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__)).replace('/src/processing', '')