import multiprocessing
import numpy as np
import spacy

from typing import Tuple
from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.utils.utils import split_text_into_paragraphs

class WordInformationIndices:
    '''
    This class will handle all operations to obtain the word information indices of a text according to Coh-Metrix.
    '''
    def __init__(self, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the word information indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self._language = language
        self._nlp = spacy.load(language, disable=['parser', 'ner'])

    def get_noun_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of nouns in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of nouns.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            nouns = (1
                     for doc in self._nlp.pipe(paragraphs,
                                               batch_size=1,
                                               disable=['parser', 'ner'],
                                               n_process=threads)
                     for token in doc
                     if token.is_alpha and token.pos_ == 'NOUN')
            
            return np.sum(nouns)

    def get_verb_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of verbs in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of verbs.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            verbs = (1
                     for doc in self._nlp.pipe(paragraphs,
                                               batch_size=1,
                                               disable=['parser', 'ner'],
                                               n_process=threads)
                     for token in doc
                     if token.is_alpha and token.pos_ == 'VERB')
            
            return np.sum(verbs)

    def get_adjective_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of adjectives in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of adjectives.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            adjectives = (1
                          for doc in self._nlp.pipe(paragraphs,
                                                    batch_size=1,
                                                    disable=['parser', 'ner'],
                                                    n_process=threads)
                          for token in doc
                          if token.is_alpha and token.pos_ == 'ADJ')
            
            return np.sum(adjectives)

    def get_adverb_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of adverbs in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of adverbs.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            adverbs = (1
                       for doc in self._nlp.pipe(paragraphs,
                                                 batch_size=1,
                                                 disable=['parser', 'ner'],
                                                 n_process=threads)
                       for token in doc
                       if token.is_alpha and token.pos_ == 'ADV')
            
            return np.sum(adverbs)

    def get_personal_pronoun_count(self, text: str, workers: int=-1) -> float:
        '''
        This method calculates the amount of presonal pronouns per 1000 words in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The amount of presonal pronouns per 1000 words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'PronType=Prs' in token.tag_)
            
            return np.sum(personal_pronouns)/1000

    def get_personal_pronoun_first_person_single_form_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of personal pronouns in first person single form in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The amount of personal pronouns in first person single form.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Sing' in token.tag_ and 'Person=1' in token.tag_)
            
            return np.sum(personal_pronouns)

    def get_personal_pronoun_first_person_plural_form_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of personal pronouns in first person plural form in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of personal pronouns in first person plural form.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Plur' in token.tag_ and 'Person=1' in token.tag_)
            
            return np.sum(personal_pronouns)

    def get_personal_pronoun_second_person_single_form_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of personal pronouns in second person single form in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of personal pronouns in second person single form.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Sing' in token.tag_ and 'Person=2' in token.tag_)
            
            return np.sum(personal_pronouns)

    def get_personal_pronoun_second_person_plural_form_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of personal pronouns in second person plural form in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of personal pronouns in second person plural form.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Plur' in token.tag_ and 'Person=2' in token.tag_)
            
            return np.sum(personal_pronouns)

    def get_personal_pronoun_third_person_singular_form_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of personal pronouns in third person singular form in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of personal pronouns in third person singular form.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Sing' in token.tag_ and 'Person=3' in token.tag_)
            
            return np.sum(personal_pronouns)

    def get_personal_pronoun_third_person_plural_form_count(self, text: str, workers: int=-1) -> int:
        '''
        This method calculates the amount of personal pronouns in third person plural form in a text.

        Parameters:
        text(str): The text to be analyzed.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The amount of personal pronouns in third person plural form.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            
            if self._language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Plur' in token.tag_ and 'Person=3' in token.tag_)
            
            return np.sum(personal_pronouns)
