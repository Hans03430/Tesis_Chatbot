import multiprocessing

from typing import Tuple

import numpy as np
import spacy

from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.pipes.noun_phrase_tagger import NounPhraseTagger
from src.processing.utils.utils import split_text_into_paragraphs


class SyntacticComplexityIndices:
    '''
    This class will handle all operations to find the synthactic complexity indices of a text according to Coh-Metrix.
    '''

    def __init__(self, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the synthactic complexity indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self.language = language
        self._nlp = spacy.load(language, disable=['ner'])
        self._nlp.add_pipe(self._nlp.create_pipe('sentencizer'))
        self._nlp.add_pipe(NounPhraseTagger(language), after='parser')

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
            
            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['sentencizer', 'ner'], n_process=threads): # Calculate with multiprocessing 
                for nph in doc._.noun_phrases:
                    modifiers_per_noun_phrase.append(sum(1
                                                         for token in nph
                                                         if token.pos_ == 'ADJ'))

        
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
            
            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['noun phrase tagger', 'ner'], n_process=threads): # Calculate with multiprocessing 
                for sent in doc.sents:
                    left_words = []
                    for token in sent:
                        if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                            break
                        else:
                            left_words.append(token.text)
                
                    words_before_main_verb.append(len(left_words))
        
            return np.mean(words_before_main_verb)