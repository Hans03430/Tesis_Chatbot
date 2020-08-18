import multiprocessing

import spacy

from src.processing.coh_metrix_indices.descriptive_indices import DescriptiveIndices
from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.pipes.noun_phrase_tagger import NounPhraseTagger
from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger
from src.processing.pipes.negative_expression_tagger import NegativeExpressionTagger
from src.processing.utils.utils import split_text_into_paragraphs


class SyntacticPatternDensityIndices:
    '''
    This class will handle all operations to find the synthactic pattern density indices of a text according to Coh-Metrix.
    '''

    def __init__(self, language: str='es', descriptive_indices: DescriptiveIndices=None) -> None:
        '''
        The constructor will initialize this object that calculates the synthactic pattern density indices for a specific language of those that are available.

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
        self._nlp = spacy.load(language, disable=['ner'])
        self._nlp.add_pipe(NounPhraseTagger(language), after='parser')
        self._nlp.add_pipe(VerbPhraseTagger(self._nlp, language), after='noun phrase tagger')
        self._nlp.add_pipe(NegativeExpressionTagger(self._nlp, language), after='verb phrase tagger')
        self._incidence = 1000

        if descriptive_indices is None: # Assign the descriptive indices to an attribute
            self._di = DescriptiveIndices(language)
        else:
            self._di = descriptive_indices

    def get_noun_phrase_density(self, text: str, word_count: int=None, workers: int=-1) -> int:
        '''
        This function obtains the incidence of noun phrases that exist on a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analized.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The incidence of noun phrases per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)            
            noun_phrase_density = 0
            
            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['verb phrase tagger', 'negative expression tagger', 'ner'], n_process=threads): # Calculate with multiprocessing 
                noun_phrase_density += len(doc._.noun_phrases)
            
            return (noun_phrase_density / wc) * self._incidence

    def get_verb_phrase_density(self, text: str, word_count: int=None, workers: int=-1) -> int:
        '''
        This function obtains the incidence of verb phrases that exist on a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analized.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The incidence of verb phrases per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)            
            verb_phrases_density = 0

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['noun phrase tagger', 'negative expression tagger', 'parser', 'ner'], n_process=threads): # Calculate with multiprocessing
                verb_phrases_density += len(doc._.verb_phrases)

            return (verb_phrases_density / wc) * self._incidence
            

    def get_negative_expressions_density(self, text: str, word_count: int=None, workers: int=-1) -> int:
        '''
        This function obtains the incidence of negative expressions that exist on a text per {self._incidence} words.

        Parameters:
        text(str): The text to be analized.
        word_count(int): The amount of words in the text.
        workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used.

        Returns:
        int: The incidence of negative expressions per {self._incidence} words.
        '''
        if len(text) == 0:
            raise ValueError('The word is empty.')
        elif workers == 0 or workers < -1:
            raise ValueError('Workers must be -1 or any positive number greater than 0')
        else:
            paragraphs = split_text_into_paragraphs(text) # Find all paragraphs
            threads = multiprocessing.cpu_count() if workers == -1 else workers
            wc = word_count if word_count is not None else self._di.get_word_count_from_text(text)            
            negative_expressions_density = 0

            for doc in self._nlp.pipe(paragraphs, batch_size=threads, disable=['verb phrase tagger', 'noun phrase tagger', 'parser', 'ner'], n_process=threads): # Calculate with multiprocessing
                negative_expressions_density += len(doc._.negation_expressions)

            return (negative_expressions_density / wc) * self._incidence