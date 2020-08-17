import multiprocessing
import numpy as np
import pyphen
import spacy
import statistics
import string

from itertools import chain
from itertools import repeat
from spacy.lang.es import Spanish
from spacy.util import get_lang_class
from typing import List

from src.processing.constants import ACCEPTED_LANGUAGES, LANGUAGES_DICTIONARY_PYPHEN
from src.processing.pipes.causal_connectives_tagger import CausalConnectivesTagger
from src.processing.pipes.logical_connectives_tagger import LogicalConnectivesTagger
from src.processing.pipes.adversative_connectives_tagger import AdversativeConnectivesTagger
from src.processing.pipes.temporal_connectives_tagger import TemporalConnectivesTagger
from src.processing.pipes.additive_connectives_tagger import AdditiveConnectivesTagger
from src.processing.utils.utils import split_text_into_paragraphs
from src.processing.utils.utils import split_text_into_sentences

class ConnectiveIndices:
    '''
    This class will handle all operations to obtain the connective indices of a text according to Coh-Metrix
    '''
    def __init__(self, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the connective indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self.language = language
        self._nlp = spacy.load(language, disable=['parser', 'ner'])
        self._nlp.add_pipe(CausalConnectivesTagger(self._nlp, language), after='tagger')
        self._nlp.add_pipe(LogicalConnectivesTagger(self._nlp, language), after='tagger')
        self._nlp.add_pipe(AdversativeConnectivesTagger(self._nlp, language), after='tagger')
        self._nlp.add_pipe(TemporalConnectivesTagger(self._nlp, language), after='tagger')
        self._nlp.add_pipe(AdditiveConnectivesTagger(self._nlp, language), after='tagger')
        self._index_amount = 1000

    def get_causal_connectives_incidence(self, text: str, workers: int=-1) -> float:
        """
        This method returns the incidence per {index_ammount} words for causal connectives.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: Amount of causal connectives per {index_ammount} words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            connectives = (len(doc._.causal_connectives)
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=1,
                                                     disable=['parser', 'ner', 'logical connective tagger', 'adversative connective tagger', 'temporal connective tagger', 'additive connective tagger'],
                                                     n_process=threads))
            
            return np.sum(connectives) / self._index_amount

    def get_logical_connectives_incidence(self, text: str, workers: int=-1) -> float:
        """
        This method returns the incidence per {index_ammount} words for logical connectives.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: Amount of logical connectives per {index_ammount} words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            connectives = (len(doc._.logical_connectives)
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=1,
                                                     disable=['parser', 'ner', 'causal connective tagger', 'adversative connective tagger', 'temporal connective tagger', 'additive connective tagger'],
                                                     n_process=threads))
            
            return np.sum(connectives) / self._index_amount

    def get_adversative_connectives_incidence(self, text: str, workers: int=-1) -> float:
        """
        This method returns the incidence per {index_ammount} words for adversative connectives.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: Amount of adversative connectives per {index_ammount} words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            connectives = (len(doc._.adversative_connectives)
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=1,
                                                     disable=['parser', 'ner', 'causal connective tagger', 'logical connective tagger', 'temporal connective tagger', 'additive connective tagger'],
                                                     n_process=threads))
            
            return np.sum(connectives) / self._index_amount

    def get_temporal_connectives_incidence(self, text: str, workers: int=-1) -> float:
        """
        This method returns the incidence per {index_ammount} words for temporal connectives.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: Amount of temporal connectives per {index_ammount} words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            connectives = (len(doc._.temporal_connectives)
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=1,
                                                     disable=['parser', 'ner', 'causal connective tagger', 'logical connective tagger', 'adversative connective tagger', 'additive connective tagger'],
                                                     n_process=threads))
            
            return np.sum(connectives) / self._index_amount

    def get_additive_connectives_incidence(self, text: str, workers: int=-1) -> float:
        """
        This method returns the incidence per {index_ammount} words for additive connectives.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: Amount of additive connectives per {index_ammount} words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            connectives = (len(doc._.additive_connectives)
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=1,
                                                     disable=['parser', 'ner', 'causal connective tagger', 'logical connective tagger', 'adversative connective tagger', 'temporal connective tagger'],
                                                     n_process=threads))
            
            return np.sum(connectives) / self._index_amount

    def get_all_connectives_incidence(self, text: str, workers: int=-1) -> float:
        """
        This method returns the incidence per {index_ammount} words for all connectives.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: Amount of all connectives per {index_ammount} words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            connectives = (sum([len(doc._.causal_connectives), len(doc._.logical_connectives), len(doc._.adversative_connectives), len(doc._.temporal_connectives), len(doc._.additive_connectives)])
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=1,
                                                     disable=['parser', 'ner'],
                                                     n_process=threads))
            
            return np.sum(connectives) / self._index_amount