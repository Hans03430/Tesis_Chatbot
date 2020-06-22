import multiprocessing

from typing import Tuple

import spacy

from spacy.matcher import Matcher
from spacy.util import filter_spans

from src.processing.coh_metrix_indices.descriptive_indices import split_text_into_paragraphs
from src.processing.coh_metrix_indices.descriptive_indices import split_text_into_sentences
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

    sentences = split_text_into_sentences(text, language) # Find all sentences
    cpu_count = multiprocessing.cpu_count()
    noun_phrase_density = 0
    for doc in nlp.pipe(sentences, batch_size=cpu_count**2, disable=['ner'], n_process=cpu_count): # Calculate with multiprocessing 
        noun_phrases = set()    
        for nc in doc.noun_chunks: # We find the noun phrases in the entire document
            for np in [nc, doc[nc.root.left_edge.i:nc.root.right_edge.i+1]]:
                noun_phrases.add(np)

        noun_phrase_density += len(filter_spans(noun_phrases))
    
    return noun_phrase_density

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

    nlp = spacy.load('es', disable=['parser', 'ner'])
    matcher = Matcher(nlp.vocab)
    pattern = []
    # doc = nlp(text)

    if language == 'es': # Verb phrases for spanish
        pattern = [{'POS': 'AUX', },
                   {'POS': 'CONJ', 'OP': '*'},
                   {'POS': 'ADP', 'TAG': 'ADP__AdpType=Prep', 'OP': '*'},
                   {'POS': 'VERB'}] # The pattern for verb phrases in spanish
    else: # Support for future languages
        pass

    matcher.add('Verb phrase', None, pattern) # Add the verb phrase pattern
    
    sentences = split_text_into_sentences(text, language) # Find all sentences
    verb_phrases_density = 0
    cpu_count = multiprocessing.cpu_count()
    for doc in nlp.pipe(sentences, batch_size=cpu_count**2, disable=['parser', 'ner'], n_process=cpu_count): # Calculate with multiprocessing
        matches = matcher(doc)
        spans = [doc[start:end] for _, start, end in matches]
        verb_phrases_density += len(filter_spans(spans))

    return verb_phrases_density
        

def get_negative_expressions_density(text: str, language: str='es') -> int:
    '''
    This function obtains the amount of negative expressions that exist on a text.

    Parameters:
    text(str): The text to be split into sentences.
    language(str): The language of the text.

    Returns:
    int: The ammount of negative expressions.
    '''
    if len(text) == 0:
        raise ValueError('The word is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    nlp = spacy.load('es', disable=['parser', 'ner'])
    matcher = Matcher(nlp.vocab)
    pattern = []
    # doc = nlp(text)

    if language == 'es': # Verb phrases for spanish
        pattern = [{'POS': 'ADV', 
                    'LOWER': {
                        'IN': ['no', 'nunca', 'jamás', 'tampoco']
                        }
                    }] # The pattern for negation expressions
    else: # Support for future languages
        pass

    matcher.add('Negation expressions', None, pattern) # Add the verb phrase pattern
    sentences = split_text_into_sentences(text, language) # Find all sentences
    negative_expressions_density = 0
    cpu_count = multiprocessing.cpu_count()
    for doc in nlp.pipe(sentences, batch_size=cpu_count**2, disable=['parser', 'ner'], n_process=cpu_count): # Calculate with multiprocessing
        matches = matcher(doc)
        spans = [doc[start:end] for _, start, end in matches]
        negative_expressions_density += len(filter_spans(spans))

    return negative_expressions_density