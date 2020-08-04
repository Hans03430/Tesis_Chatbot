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
from src.processing.pipes.syllable_splitter import SyllableSplitter
from src.processing.utils.utils import split_text_into_paragraphs
from src.processing.utils.utils import split_text_into_sentences

class DescriptiveIndices:
    '''
    This class will handle all operations to obtain the descriptive indices of a text according to Coh-Metrix
    '''
    def __init__(self, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the descriptive indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self._language = language
        self._nlp = spacy.load(language, disable=['tagger', 'parser', 'ner'])
        self._nlp.add_pipe(self._nlp.create_pipe('sentencizer'))
        self._nlp.add_pipe(SyllableSplitter(language), after='sentencizer')

    def get_paragraph_count_from_text(self, text: str) -> int:
        """
        This function counts how many paragarphs are there in a text

        Parameters:
        text(str): The text to be analyzed

        Returns:
        int: The amount of paragraphs in a text
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        
        return len(split_text_into_paragraphs(text))

    def get_sentence_count_from_text(self, text: str, workers: int=-1) -> int:
        """
        This function counts how many sentences a text has.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of sentences.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            sentences = (1
                        for doc in self._nlp.pipe(paragraphs,
                                                  batch_size=1,
                                                  disable=['syllable splitter', 'parser', 'tagger', 'ner'],
                                                  n_process=threads)
                        for sentence in doc.sents)
            
            return np.sum(sentences)

    def get_word_count_from_text(self, text: str, workers: int=-1) -> int:
        """
        This function counts how many words a text has.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of words.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers

            total_words = (1
                           for doc in self._nlp.pipe(paragraphs,
                                                     batch_size=threads,
                                                     disable=['syllable splitter', 'parser', 'tagger', 'ner'],
                                                     n_process=threads)
                           for token in doc
                           if token.is_alpha)

            return np.sum(total_words)

    def get_mean_of_length_of_paragraphs(self, text: str, workers: int=-1) -> float:
        """
        This function returns the average numbers of sentences in each paragraph.

        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The mean of the amount in sentences in each paragraph.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            sentences_per_paragraph = [sum(1 for _ in doc.sents)
                                       for doc in self._nlp.pipe(paragraphs,
                                                                 batch_size=threads,
                                                                 disable=['syllable splitter', 'parser', 'tagger', 'ner'],
                                                                 n_process=threads)]

            return np.mean(sentences_per_paragraph)

    def get_std_of_length_of_paragraphs(self, text: str, workers: int=-1) -> float:
        """
        This function returns the standard deviation of the mean of sentences of each paragraph.

        text(str): The text to be anaylized.
        language(str): The language of the text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The standard deviation of the mean of the amount in sentences in each paragraph.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            sentences_per_paragraph = [sum(1 for _ in doc.sents)
                                       for doc in self._nlp.pipe(paragraphs,
                                                                 batch_size=threads,
                                                                 disable=['syllable splitter', 'parser', 'tagger', 'ner'],
                                                                 n_process=threads)]

            return np.std(sentences_per_paragraph)

    def get_mean_of_length_of_sentences(self, text: str, workers: int=-1) -> float:
        """
        This function returns the average amount of words in each sentence.

        Parameters:
        text(str): The text to be anaylized.
        language(str): The language of the text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The mean of the amount in words in each sentence.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            words_per_sentence = [sum(1 for _ in sentence) 
                                  for doc in self._nlp.pipe(paragraphs,
                                                            batch_size=threads,
                                                            disable=['syllable splitter', 'parser', 'tagger', 'ner'],
                                                            n_process=threads)
                                  for sentence in doc.sents]

            return np.mean(words_per_sentence)

    def get_std_of_length_of_sentences(self, text: str, workers: int=-1) -> float:
        """
        This function returns the standard deviation of the amount of words in each sentence.

        Parameters:
        text(str): The text to be anaylized
        language(str): The language of the text to be analyzed
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

        Returns:
        float: The standard deviation of the amount in words in each sentence.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            words_per_sentence = [sum(1 for _ in sentence) 
                                  for doc in self._nlp.pipe(paragraphs,
                                                            batch_size=threads,
                                                            disable=['syllable splitter', 'parser', 'tagger', 'ner'],
                                                            n_process=threads)
                                  for sentence in doc.sents]

            return np.std(words_per_sentence)

    def get_mean_of_length_of_words(self, text: str, workers: int=-1) -> float:
        """
        This function returns the average amount of letters in each word.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The mean of the amount in letters in each word.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            letters_per_word = [len(token)
                                for doc in self._nlp.pipe(paragraphs,
                                                          batch_size=threads,
                                                          disable=['sentencizer', 'syllable splitter', 'parser', 'tagger', 'ner'],
                                                          n_process=threads)
                                for token in doc
                                if token.is_alpha]

            return np.mean(letters_per_word)

    def get_std_of_length_of_words(self, text: str, workers=-1) -> float:
        """
        This function returns the standard deviation of the amount of letters in each word.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The standard deviation of the amount in letters in each word.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            letters_per_word = [len(token)
                                for doc in self._nlp.pipe(paragraphs,
                                                          batch_size=threads,
                                                          disable=['sentencizer', 'syllable splitter', 'parser', 'tagger', 'ner'],
                                                          n_process=threads)
                                for token in doc
                                if token.is_alpha]

            return np.std(letters_per_word)

    def get_mean_of_syllables_per_word(self, text: str, workers=-1) -> float:
        """
        This function returns the average amount of syllables in each word.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The mean of the amount in syllables in each word.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers

            syllables_per_word = [len(token._.syllables)
                                  for doc in self._nlp.pipe(paragraphs,
                                                          batch_size=threads,
                                                          disable=['sentencizer', 'parser', 'tagger', 'ner'],
                                                          n_process=threads)
                                  for token in doc
                                  if token.is_alpha and token._.syllables is not None]

            return np.mean(syllables_per_word)

    def get_std_of_syllables_per_word(self, text: str,  workers=-1) -> float:
        """
        This function returns the standard deviation of the amount of syllables in each word.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The standard deviation of the amount in syllables in each word.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers

            syllables_per_word = [len(token._.syllables)
                                  for doc in self._nlp.pipe(paragraphs,
                                                          batch_size=threads,
                                                          disable=['sentencizer', 'parser', 'tagger', 'ner'],
                                                          n_process=threads)
                                  for token in doc
                                  if token.is_alpha and token._.syllables is not None]

            return np.std(syllables_per_word)
