import multiprocessing
import numpy as np
import spacy

from typing import Tuple

from src.processing.coh_metrix_indices.descriptive_indices import DescriptiveIndices
from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.utils.utils import split_text_into_paragraphs

class WordInformationIndices:
    '''
    This class will handle all operations to obtain the word information indices of a text according to Coh-Metrix.
    '''
    def __init__(self, language: str='es', descriptive_indices: DescriptiveIndices=None) -> None:
        '''
        The constructor will initialize this object that calculates the word information indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.
        descriptive_indices(DescriptiveIndices): The class that calculates the descriptive indices of a text in a certain language.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        elif descriptive_indices is not None and descriptive_indices.language != language:
            raise ValueError(f'The descriptive indices analyzer must be of the same language as the word information analyzer.')
        
        self.language = language
        self._nlp = spacy.load(language, disable=['parser', 'ner'])
        self._incidence = 1000

        if descriptive_indices is None: # Assign the descriptive indices to an attribute
            self._di = DescriptiveIndices(language)
        else:
            self._di = descriptive_indices

    def get_noun_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of nouns in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of nouns per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            nouns = (1
                     for doc in self._nlp.pipe(paragraphs,
                                               batch_size=1,
                                               disable=['parser', 'ner'],
                                               n_process=threads)
                     for token in doc
                     if token.is_alpha and token.pos_ == 'NOUN')
            
            return (np.sum(nouns) / wc) * self._incidence

    def get_verb_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of verbs in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of verbs per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            verbs = (1
                     for doc in self._nlp.pipe(paragraphs,
                                               batch_size=1,
                                               disable=['parser', 'ner'],
                                               n_process=threads)
                     for token in doc
                     if token.is_alpha and token.pos_ == 'VERB')
            
            return (np.sum(verbs) / wc) * self._incidence

    def get_adjective_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of adjectives in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of adjectives per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            adjectives = (1
                          for doc in self._nlp.pipe(paragraphs,
                                                    batch_size=1,
                                                    disable=['parser', 'ner'],
                                                    n_process=threads)
                          for token in doc
                          if token.is_alpha and token.pos_ == 'ADJ')
            
            return (np.sum(adjectives) / wc) * self._incidence

    def get_adverb_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of adverbs in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of adverbs per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            adverbs = (1
                       for doc in self._nlp.pipe(paragraphs,
                                                 batch_size=1,
                                                 disable=['parser', 'ner'],
                                                 n_process=threads)
                       for token in doc
                       if token.is_alpha and token.pos_ == 'ADV')
            
            return (np.sum(adverbs) / wc) * self._incidence

    def get_personal_pronoun_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'PronType=Prs' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence

    def get_personal_pronoun_first_person_singular_form_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in first person and singular form in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns in first person and singular form per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Sing' in token.tag_ and 'Person=1' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence

    def get_personal_pronoun_first_person_plural_form_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in first person and plural form in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns in first person and plural form per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Plur' in token.tag_ and 'Person=1' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence

    def get_personal_pronoun_second_person_singular_form_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in second person and singular form in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns in second person and singular form per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Sing' in token.tag_ and 'Person=2' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence

    def get_personal_pronoun_second_person_plural_form_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in second person and plural form in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns in second person and plural form per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Plur' in token.tag_ and 'Person=2' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence

    def get_personal_pronoun_third_person_singular_form_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in third person and singular form in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns in third person and singular form per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Sing' in token.tag_ and 'Person=3' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence

    def get_personal_pronoun_third_person_plural_form_incidence(self, text: str, word_count: int=None, workers: int=-1) -> float:
        '''
        This method calculates the incidence of personal pronouns in third person and plural form in a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The incidence of personal pronouns in third person and plural form per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)
            
            if self.language == 'es': # For spanish
                personal_pronouns = (1
                                     for doc in self._nlp.pipe(paragraphs,
                                                               batch_size=1,
                                                               disable=['parser', 'ner'],
                                                               n_process=threads)
                                     for token in doc
                                     if token.is_alpha and 'Number=Plur' in token.tag_ and 'Person=3' in token.tag_)
            
            return (np.sum(personal_pronouns) / wc) * self._incidence
