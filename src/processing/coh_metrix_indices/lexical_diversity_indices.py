import multiprocessing
import spacy
import string

from src.processing.constants import ACCEPTED_LANGUAGES, LANGUAGES_DICTIONARY_PYPHEN
from src.processing.utils.utils import split_text_into_paragraphs

class LexicalDiversityIndices:
    '''
    This class will handle all operations to obtain the lexical diversity indices of a text according to Coh-Metrix
    '''
    def __init__(self, language: str='es') -> None:
        '''
        The constructor will initialize this object that calculates the lexical diversity indices for a specific language of those that are available.

        Parameters:
        language(str): The language that the texts to process will have.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self.language = language
        self._nlp = spacy.load(language, disable=['parser', 'ner'])

    def get_type_token_ratio_between_all_words(self, text: str, workers=-1) -> float:
        """
        This method returns the type token ratio between all words of a text.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The type token ratio between all words of a text.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            tokens = []

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'ner'], n_process=threads):
                for token in doc:
                    if token.is_alpha: # Gather all tokens in lowercase
                        tokens.append(token.text.lower())

            return len(set(tokens)) / len(tokens)

    def get_type_token_ratio_of_content_words(self, text: str, workers=-1) -> float:
        """
        This method returns the type token ratio of content words of a text. Content words are nouns, verbs, adjectives and adverbs.

        Parameters:
        text(str): The text to be anaylized.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        float: The type token ratio betweeof content of a text.
        """
        if len(text) == 0:
            raise ValueError('The text is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            tokens = []

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'ner'], n_process=threads):
                for token in doc:
                    if token.is_alpha and token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV']: # Gather all nouns, verbs, adjectives or adverbs in lowercase
                        tokens.append(token.text.lower())

            return len(set(tokens)) / len(tokens)