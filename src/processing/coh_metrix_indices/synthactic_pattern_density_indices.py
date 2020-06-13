import spacy

from typing import Tuple

from spacy.matcher import Matcher
from spacy.util import filter_spans

from src.processing.constants import ACCEPTED_LANGUAGES

def get_noun_phrase_density(text: str, language: str='es') -> int:
    '''
    This function obtains the amount of noun phrases that exist on a text.

    Parameters:
    text(str): The text to be split into sentences.
    language(str): The language of the text.

    Returns:
    int: The ammount of noun phrases
    '''
    if len(text) == 0:
        raise ValueError('The word is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    nlp = spacy.load('es', disable=['ner'])
    doc = nlp(text)

    noun_pharses = set()    
    for nc in doc.noun_chunks: # We find the noun phrases in the entire document
        for np in [nc, doc[nc.root.left_edge.i:nc.root.right_edge.i+1]]:
            noun_pharses.add(np)

    return len(filter_spans(noun_pharses))

def get_verb_phrase_density(text: str, language: str='es') -> int:
    '''
    This function obtains the amount of verb phrases that exist on a text.

    Parameters:
    text(str): The text to be split into sentences.
    language(str): The language of the text.

    Returns:
    int: The ammount of verb phrases
    '''
    if len(text) == 0:
        raise ValueError('The word is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    nlp = spacy.load('es', disable=['ner'])
    matcher = Matcher(nlp.vocab)
    pattern = []
    doc = nlp(text)

    if language == 'es': # Verb phrases for spanish
        pattern = [{'POS': 'AUX', },
                   {'POS': 'CONJ', 'OP': '*'},
                   {'POS': 'ADP', 'TAG': 'ADP__AdpType=Prep', 'OP': '*'},
                   {'POS': 'VERB'}] # The pattern for verb phrases in spanish
    else: # Support for future languages
        pass

    matcher.add('Verb phrase', None, pattern) # Add the verb phrase pattern
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]

    return filter_spans(spans)
        
