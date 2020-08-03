import multiprocessing

from typing import Tuple

import spacy

from spacy.matcher import Matcher
from spacy.util import filter_spans

from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.pipes.noun_phrase_tagger import NounPhraseTagger
from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger
from src.processing.pipes.negative_expression_tagger import NegativeExpressionTagger
from src.processing.utils.utils import split_text_into_paragraphs
from src.processing.utils.utils import split_text_into_sentences


class SynthacticPatternDensityIndices:
    '''
    This class will handle all operations to find the synthactic pattern density indices of a text according to Coh-Metrix.
    '''

    def __init__(self, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the synthactic pattern density indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self._language = language
        self._nlp = spacy.load(language, disable=['ner'])
        self._nlp.add_pipe(NounPhraseTagger(language), after='parser')
        self._nlp.add_pipe(VerbPhraseTagger(self._nlp, language), after='noun phrase tagger')
        self._nlp.add_pipe(NegativeExpressionTagger(self._nlp, language), after='verb phrase tagger')

    def get_noun_phrase_density(self, text: str, workers: int=-1) -> int:
        '''
        This function obtains the amount of noun phrases that exist on a text.

        Parameters:
        text(str): The text to be analized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The ammount of noun phrases.
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            noun_phrase_density = 0

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['verb phrase tagger', 'negative expression tagger', 'ner'], n_process=threads): # Calculate with multiprocessing 
                noun_phrase_density += len(doc._.noun_phrases)
            
            return noun_phrase_density

    def get_verb_phrase_density(self, text: str, workers: int=-1) -> int:
        '''
        This function obtains the amount of verb phrases that exist on a text.

        Parameters:
        text(str): The text to be split into sentences.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The ammount of verb phrases
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            verb_phrases_density = 0

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['noun phrase tagger', 'negative expression tagger', 'parser', 'ner'], n_process=threads): # Calculate with multiprocessing
                verb_phrases_density += len(doc._.verb_phrases)

            return verb_phrases_density
            

    def get_negative_expressions_density(self, text: str, workers: int=-1) -> int:
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
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all sentences
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            negative_expressions_density = 0

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['verb phrase tagger', 'noun phrase tagger', 'parser', 'ner'], n_process=threads): # Calculate with multiprocessing
                negative_expressions_density += len(doc._.negation_expressions)

            return negative_expressions_density