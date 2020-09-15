import multiprocessing

from typing import Tuple

import numpy as np
import spacy

from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.utils.utils import is_word
from src.processing.utils.utils import split_text_into_paragraphs


class SyntacticComplexityIndices:
    '''
    This class will handle all operations to find the synthactic complexity indices of a text according to Coh-Metrix.
    '''

    def __init__(self, nlp, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the synthactic complexity indices for a specific language of those that are available.

        Parameters:
        nlp: The spacy model that corresponds to a language.
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self.language = language
        self._nlp = nlp

    def get_mean_number_of_modifiers_per_noun_phrase(self, text: str, workers: int=-1) -> float:
        '''
        This method calculates the mean number of modifiers per noun phrase in a text.

        Parameters:
        text(str): The text to be analized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The mean of modifiers per noun phrases.
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            modifiers_per_noun_phrase = []
            disable_pipeline = [pipe for pipe in self._nlp.pipe_names if pipe not in ['parser', 'tagger', 'noun phrase tagger']]

            modifiers_per_noun_phrase = [sum(1 for token in nph if token.pos_ == 'ADJ')
                                         for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=disable_pipeline, n_process=threads)
                                         for nph in doc._.noun_phrases]

            return np.mean(modifiers_per_noun_phrase)

    def get_mean_number_of_words_before_main_verb(self, text: str, workers: int=-1) -> float:
        '''
        This method calculates the mean number of words before the main verb of sentences.

        Parameters:
        text(str): The text to be analized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The mean of words before the main verb of sentences.
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            words_before_main_verb = []
            disable_pipeline = [pipe for pipe in self._nlp.pipe_names if pipe not in ['parser', 'tagger']]
            
            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=disable_pipeline, n_process=threads): # Calculate with multiprocessing 
                for sent in doc.sents:
                    left_words = []
                    for token in sent:
                        if token.pos_ in ['VERB', 'AUX'] and token.dep_ == 'ROOT':
                            break
                        else:
                            if is_word(token):
                                left_words.append(token.text)
                                
                    words_before_main_verb.append(len(left_words))
        
            return np.mean(words_before_main_verb)