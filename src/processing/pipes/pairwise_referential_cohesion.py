import pyphen

from spacy.tokens import Doc
from spacy.tokens import Token

from src.processing.constants import ACCEPTED_LANGUAGES

Doc.set_extension('referential_cohesion', default=None, force=True)

class PairwiseReferentialCohesion:
    name = 'pairwise referential cohesion'

    def __init__(self, language: str='es') -> None:
        '''
        This constructor will initialize the object that calculating referential cohesion. It goes after sentencizer.

        Parameters:
        language: The language that this pipeline will be used in.

        Returns:
        None.
        '''
        if not language in ACCEPTED_LANGUAGES:
            raise ValueError(f'Language {language} is not supported yet')

        self._language = language
        self.sentence_analyzer = None

    def __call__(self, doc: Doc) -> Doc:
        '''
        This method will calculate the referential cohesion between a pair of sentences, according to a sentence_analyzer function that takes two sentences and a language.

        Parameters:
        doc(Doc): A Spacy document.
        '''

        if self.sentence_analyzer is None:
            raise AttributeError('The sentence_analyzer function to calculate referential cohesion between two sentences hasn\'t been specified')
        
        sentence_length = sum(1 for _ in doc.sents)
        if sentence_length != 2:
            raise AttributeError(f'The referential cohesion is calculated for only two sentences. Current amount of sentences is {sentence_length}')

        sentences = list(doc.sents)
        prev = sentences[0]
        cur = sentences[1]

        doc._.referential_cohesion = self.sentence_analyzer(prev, cur, self._language)
        
        return doc