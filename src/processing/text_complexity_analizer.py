import time

from typing import Dict
from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.coh_metrix_indices.connective_indices import ConnectiveIndices
from src.processing.coh_metrix_indices.descriptive_indices import DescriptiveIndices
from src.processing.coh_metrix_indices.lexical_diversity_indices import LexicalDiversityIndices
from src.processing.coh_metrix_indices.readability_indices import ReadabilityIndices
from src.processing.coh_metrix_indices.syntactic_complexity_indices import SyntacticComplexityIndices
from src.processing.coh_metrix_indices.syntactic_pattern_density_indices import SyntacticPatternDensityIndices
from src.processing.coh_metrix_indices.word_information_indices import WordInformationIndices


class TextComplexityAnalizer:
    '''
    This class groups all of the indices in order to calculate them in one go. It works for a specific language.
    '''
    def __init__(self, language:str = 'es') -> None:
        '''
        This constructor initializes the analizer for a specific language.

        Parameters:
        language(str): The language that the texts are in.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')
        
        self.language = language
        self._di = DescriptiveIndices(language)
        self._spdi = SyntacticPatternDensityIndices(language, self._di)
        self._wii = WordInformationIndices(language, self._di)
        self._sci = SyntacticComplexityIndices(language)
        self._ci = ConnectiveIndices(language)
        self._ldi = LexicalDiversityIndices(language)
        self._ri = ReadabilityIndices(language)

    def calculate_descriptive_indices_for_one_text(self, text: str) -> Dict:
        '''
        This method calculates the descriptive indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.

        Returns:
        Dict: The dictionary with the descriptive indices.
        '''
        indices = {}
        indices['DESPC'] = self._di.get_paragraph_count_from_text(text=text)
        indices['DESSC'] = self._di.get_sentence_count_from_text(text=text)
        indices['DESWC'] = self._di.get_word_count_from_text(text=text)
        indices['DESPL'] = self._di.get_mean_of_length_of_paragraphs(text=text)
        indices['DESPLd'] = self._di.get_std_of_length_of_paragraphs(text=text)
        indices['DESSL'] = self._di.get_mean_of_length_of_sentences(text=text)
        indices['DESSLd'] = self._di.get_std_of_length_of_sentences(text=text)
        indices['DESWLsy'] = self._di.get_mean_of_syllables_per_word(text=text)
        indices['DESWLsyd'] = self._di.get_std_of_syllables_per_word(text=text)
        indices['DESWLlt'] = self._di.get_mean_of_length_of_words(text=text)
        indices['DESWLltd'] = self._di.get_std_of_length_of_words(text=text)
        return indices

    def calculate_word_information_indices_for_one_text(self, text: str, word_count: int=None) -> Dict:
        '''
        This method calculates the descriptive indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words that the current text has in order to calculate the incidence.

        Returns:
        Dict: The dictionary with the word information indices.
        '''
        indices = {}
        indices['WRDNOUN'] = self._wii.get_noun_incidence(text=text, word_count=word_count)
        indices['WRDVERB'] = self._wii.get_verb_incidence(text=text, word_count=word_count)
        indices['WRDADJ'] = self._wii.get_adjective_incidence(text=text, word_count=word_count)
        indices['WRDADV'] = self._wii.get_adverb_incidence(text=text, word_count=word_count)
        indices['WRDPRO'] = self._wii.get_personal_pronoun_incidence(text=text, word_count=word_count)
        indices['WRDPRP1s'] = self._wii.get_personal_pronoun_first_person_singular_form_incidence(text=text, word_count=word_count)
        indices['WRDPRP1p'] = self._wii.get_personal_pronoun_first_person_plural_form_incidence(text=text, word_count=word_count)
        indices['WRDPRP2s'] = self._wii.get_personal_pronoun_second_person_singular_form_incidence(text=text, word_count=word_count)
        indices['WRDPRP2p'] = self._wii.get_personal_pronoun_second_person_plural_form_incidence(text=text, word_count=word_count)
        indices['WRDPRP3s'] = self._wii.get_personal_pronoun_third_person_singular_form_incidence(text=text, word_count=word_count)
        indices['WRDPRP3p'] = self._wii.get_personal_pronoun_third_person_plural_form_incidence(text=text, word_count=word_count)
        
        return indices

    def calculate_syntactic_pattern_density_indices_for_one_text(self, text: str, word_count: int=None) -> Dict:
        '''
        This method calculates the syntactic pattern indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words that the current text has in order to calculate the incidence.

        Returns:
        Dict: The dictionary with the syntactic pattern indices.
        '''
        indices = {}
        indices['DRNP'] = self._spdi.get_noun_phrase_density(text=text, word_count=word_count)
        indices['DRVP'] = self._spdi.get_verb_phrase_density(text=text, word_count=word_count)
        indices['DRNEG'] = self._spdi.get_negation_expressions_density(text=text, word_count=word_count)

        return indices
        
    def calculate_syntactic_complexity_indices(self, text: str) -> Dict:
        '''
        This method calculates the syntactic complexity indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.

        Returns:
        Dict: The dictionary with the syntactic complexity indices.
        '''
        indices = {}
        indices['SYNNP'] = self._sci.get_mean_number_of_modifiers_per_noun_phrase(text=text)

        return indices

    def calculate_connective_indices(self, text: str, word_count: int=None) -> Dict:
        '''
        This method calculates the connectives indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words that the current text has in order to calculate the incidence.

        Returns:
        Dict: The dictionary with the connectives indices.
        '''
        indices = {}
        indices['CNCAll'] = self._ci.get_all_connectives_incidence(text=text, word_count=word_count)
        indices['CNCCaus'] = self._ci.get_causal_connectives_incidence(text=text, word_count=word_count)
        indices['CNCLogic'] = self._ci.get_logical_connectives_incidence(text=text, word_count=word_count)
        indices['CNCADC'] = self._ci.get_adversative_connectives_incidence(text=text, word_count=word_count)
        indices['CNCTemp'] = self._ci.get_temporal_connectives_incidence(text=text, word_count=word_count)
        indices['CNCAdd'] = self._ci.get_additive_connectives_incidence(text=text, word_count=word_count)

        return indices

    def calculate_lexical_diversity_density_indices_for_one_text(self, text: str) -> Dict:
        '''
        This method calculates the lexical diversity indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.
        word_count(int): The amount of words that the current text has in order to calculate the incidence.

        Returns:
        Dict: The dictionary with the lexical diversity indices.
        '''
        indices = {}
        indices['LDTTRa'] = self._ldi.get_type_token_ratio_between_all_words(text=text)
        indices['LDTTRcw'] = self._ldi.get_type_token_ratio_of_content_words(text=text)

        return indices

    def calculate_readability_indices(self, text: str, mean_syllables_per_word: int=None, mean_words_per_sentence: int=None) -> Dict:
        '''
        This method calculates the readability indices and stores them in a dictionary.

        Parameters:
        text(str): The text to be analyzed.
        mean_syllables_per_word(int): The mean of syllables per word in the text.
        mean_words_per_sentence(int): The mean amount of words per sentences in the text.

        Returns:
        Dict: The dictionary with the readability indices.
        '''
        indices = {}
        
        if self.language == 'es':
            indices['RDFHGL'] = self._ri.calculate_fernandez_huertas_grade_level(text=text, mean_words_per_sentence=mean_words_per_sentence, mean_syllables_per_word=mean_syllables_per_word)

        return indices