import multiprocessing
import numpy as np
import spacy
import string

from typing import Callable
from typing import List
from src.processing.constants import ACCEPTED_LANGUAGES, LANGUAGES_DICTIONARY_PYPHEN
from src.processing.pipes.syllable_splitter import SyllableSplitter
from src.processing.utils.statistics_results import StatisticsResults
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
        
        self.language = language
        self._nlp = spacy.load(ACCEPTED_LANGUAGES[language], disable=['tagger', 'parser', 'ner'])
        self._nlp.add_pipe(self._nlp.create_pipe('sentencizer'))
        self._nlp.add_pipe(SyllableSplitter(language), after='sentencizer')

    def get_paragraph_count_from_text(self, text: str) -> int:
        """
        This method counts how many paragarphs are there in a text

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
        This method counts how many sentences a text has.

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
            sentences = 0
            for doc in self._nlp.pipe(paragraphs, batch_size=1, disable=['syllable splitter', 'parser', 'tagger', 'ner'], n_process=threads):
                for s in doc.sents:
                    sentences += 1
            
            return sentences

    def get_word_count_from_text(self, text: str, workers: int=-1) -> int:
        """
        This method counts how many words a text has.

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
            total_words = 0

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['syllable splitter', 'parser', 'tagger', 'ner'], n_process=threads):
                for token in doc:
                    if token.is_alpha:
                        total_words += 1

            return total_words

    def _get_mean_std_of_metric(self, text: str, disable_pipeline: List, counter_function: Callable, statistic_type: str='all', workers=-1) -> StatisticsResults:
        """
        This method returns the mean and/or standard deviation of a descriptive metric.

        Parameters:
        text(str): The text to be anaylized.
        disable_pipeline(List): The pipeline elements to be disabled.
        counter_function(Callable): This callable will calculate the values to add to the counter array in order to calculate the standard deviation. It receives a Spacy Doc and it should return a list or number.
        statistic_type(str): Whether to calculate the mean and/or the standard deviation. It accepts 'mean', 'std' or 'all'.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        StatisticsResults: The mean and/or standard deviation of the current metric.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif statistic_type not in ['mean', 'std', 'all']:
            raise ValueError('\'statistic_type\' can only take \'mean\', \'std\' or \'all\'.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            counter = []

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=disable_pipeline, n_process=threads):
                current_result = counter_function(doc) # Find the values to add to the counter

                if not isinstance(current_result, list): # Add any numbers
                    counter.append(current_result)
                else:
                    if len(current_result) > 0: # Only add values if its not an empty array
                        counter.extend(current_result)

            stat_results = StatisticsResults()
            if statistic_type in ['std', 'all']:
                stat_results.std = np.std(counter)
            
            if statistic_type in ['mean', 'all']:
                stat_results.mean = np.mean(counter)

            return stat_results

    def get_length_of_paragraphs(self, text: str, workers: int=-1) -> StatisticsResults:
        """
        This method returns the average amount and standard deviation of sentences in each paragraph.

        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        StatisticsResults: The mean and standard deviation of the amount in sentences in each paragraph.
        """
        
        count_length_of_paragraphs = lambda doc: sum(1 for _ in doc.sents)

        disable_pipeline = ['syllable splitter', 'parser', 'tagger', 'ner']

        return self._get_mean_std_of_metric(text, disable_pipeline=disable_pipeline, counter_function=count_length_of_paragraphs, statistic_type='all', workers=workers)

    def get_length_of_sentences(self, text: str, workers: int=-1) -> StatisticsResults:
        """
        This method returns the average amount and standard deviation of words in each sentence.

        Parameters:
        text(str): The text to be anaylized.
        language(str): The language of the text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        StatisticsResults: The mean and standard deviation of the amount in words in each sentence.
        """
        count_length_of_sentences = lambda doc: [len([1 for token in sentence
                                                     if token.is_alpha])
                                                 for sentence in doc.sents]

        disable_pipeline = ['syllable splitter', 'parser', 'tagger', 'ner']

        return self._get_mean_std_of_metric(text, disable_pipeline=disable_pipeline, counter_function=count_length_of_sentences, statistic_type='all', workers=workers)

    def get_length_of_words(self, text: str, workers: int=-1) -> StatisticsResults:
        """
        This method returns the average amount and standard deviation of letters in each word.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        StatisticsResults: The mean and standard deviation of the amount in letters in each word.
        """
        count_letters_per_word = lambda doc: [len(token)
                                              for token in doc
                                              if token.is_alpha]

        disable_pipeline = ['sentencizer', 'syllable splitter', 'parser', 'tagger', 'ner']

        return self._get_mean_std_of_metric(text, disable_pipeline=disable_pipeline, counter_function=count_letters_per_word, statistic_type='all', workers=workers)

    def get_syllables_per_word(self, text: str, workers=-1) -> StatisticsResults:
        """
        This method returns the average amount and standard deviation of syllables in each word.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        StatisticsResults: The mean and standard deviation of the amount in syllables in each word.
        """
        count_syllables_per_word = lambda doc: [len(token._.syllables)
                                                for token in doc
                                                if token.is_alpha and token._.syllables is not None]

        disable_pipeline = ['sentencizer', 'parser', 'tagger', 'ner']

        return self._get_mean_std_of_metric(text, disable_pipeline=disable_pipeline, counter_function=count_syllables_per_word, statistic_type='all', workers=workers)
