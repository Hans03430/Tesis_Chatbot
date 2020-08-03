import spacy

from typing import List

from src.processing.constants import ACCEPTED_LANGUAGES


def split_text_into_paragraphs(text: str) -> List[str]:
    """
    This function splits a text into paragraphs. It assumes paragraphs are separated by two line breaks.

    Parameters:
    text(str): The text to be split into paragraphs.

    Returns:
    List[str]: A list of paragraphs.
    """
    return text.split('\n\n')


def split_text_into_sentences(text: str, language: str='es') -> List[str]:
    """
    This function splits a text into sentences.

    Parameters:
    text(str): The text to be split into sentences.
    language(str): The language of the text.

    Returns:
    List[str]: A list of sentences.
    """
    if not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    nlp = spacy.load(language, disable=['tagger', 'parser', 'ner'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    text_spacy = nlp(text)
    return [str(sentence) for sentence in text_spacy.sents]