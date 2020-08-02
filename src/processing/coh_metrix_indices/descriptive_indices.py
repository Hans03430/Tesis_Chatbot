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
from src.processing.multiprocessing_utils import parallelize_function
from src.processing.pipes.syllable_splitter import SyllableSplitter

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


def split_sentence_into_words(sentence:str, language: str='es') -> List[str]:
    """
    This function splits a sentence into words.

    Parameters:
    sentence(str): The sentence to be split.
    language(es): The language of the sentence.
    """
    if not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    nlp = spacy.load(language, disable=['tagger', 'parser', 'ner'])
    sentence_spacy = nlp(sentence)
    return [str(token.text) 
            for token in sentence_spacy
            if not token.is_punct and not token.is_digit]


def split_word_into_syllables(word: str, language: str='es') -> List[str]:
    """
    This function splits a word into syllable.

    Parameters:
    word(str): The word so be splitted into syllables.
    language(str): The language of the word.

    Returns:
    List[str]: A list of syllables
    """
    if len(word) == 0:
        raise ValueError('The word is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    dic = pyphen.Pyphen(lang=language)

    return dic.inserted(word).split('-')


def get_syllable_count_from_word(word: str, language: str='es') -> int:
    """
    This function counts how many syllables are there in a word.

    Parameters:
    word(str): The text to be analyzed.
    language(str): The language of the word.

    Returns:
    int: The amount of syllables in a word.
    """
    if len(word) == 0:
        raise ValueError('The word is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    return len(split_word_into_syllables(word, language))

def get_paragraph_count_from_text(text: str) -> int:
    """
    This function counts how many paragarphs are there in a text

    Parameters:
    text(str): The text to be analyzed

    Returns:
    int: The amount of paragraphs in a text
    """
    if not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    return len(split_text_into_paragraphs(text))


def get_sentence_count_from_text(text: str, language: str = 'es') -> int:
    """
    This function counts how many sentences a text has

    Parameters:
    text(str): The text to be analyzed
    language(str): The language of the text to be analyzed

    Returns:
    int: The amount of sentences
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    sentences = split_text_into_sentences(text, language)
    return len(sentences)


def get_word_count_from_text(text: str, language: str='es') -> int:
    """
    This function counts how many words a text has

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    int: The amount of words
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
    sentences = split_text_into_sentences(text_without_punctuation, language)
    words_per_sentence = np.array([len(split_sentence_into_words(sentence, language)) for sentence in sentences])
    
    return np.sum(words_per_sentence)


def get_mean_of_length_of_paragraphs(text: str, language: str='es', workers: int=-1) -> float:
    """
    This function returns the average numbers of sentences in each paragraph

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The mean of the amount in sentences in each paragraph
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        
        sentences_per_paragraph = [sum(1 for _ in doc.sents)
                                for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)]

        return np.mean(sentences_per_paragraph)

def get_std_of_length_of_paragraphs(text: str, language: str='es', workers: int=-1) -> float:
    """
    This function returns the standard deviation of the mean of sentences of each paragraph

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The standard deviation of the mean of the amount in sentences in each paragraph
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        
        sentences_per_paragraph = [sum(1 for _ in doc.sents)
                                for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)]

        return np.std(sentences_per_paragraph)


def get_mean_of_length_of_sentences(text: str, language: str='es', workers: int=-1) -> float:
    """
    This function returns the average amount of words in each sentence

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The mean of the amount in words in each sentence.
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        
        words_per_sentence = [sum(1 for _ in sentence) 
                            for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)
                            for sentence in doc.sents]

        return np.mean(words_per_sentence)

def get_std_of_length_of_sentences(text: str, language: str='es', workers: int=-1) -> float:
    """
    This function returns the standard deviation of the amount of words in each sentence

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The standard deviation of the amount in words in each sentence.
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        
        words_per_sentence = [sum(1 for _ in sentence) 
                            for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)
                            for sentence in doc.sents]

        return np.std(words_per_sentence)


def get_mean_of_length_of_words(text: str, language: str='es', workers: int=-1) -> float:
    """
    This function returns the average amount of letters in each word

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The mean of the amount in letters in each word
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        
        letters_per_word = [len(word)
                            for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)
                            for word in doc
                            if not word.is_punct and not word.is_digit]

        return np.mean(letters_per_word)


def get_std_of_length_of_words(text: str, language: str='es', workers=-1) -> float:
    """
    This function returns the standard deviation of the amount of letters in each word

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The standard deviation of the amount in letters in each word
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        
        letters_per_word = [len(word)
                            for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)
                            for word in doc
                            if not word.is_punct and not word.is_digit]

        return np.std(letters_per_word)


def get_mean_of_syllables_per_word(text: str, language: str='es', workers=-1) -> float:
    """
    This function returns the average amount of syllables in each word

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The mean of the amount in syllables in each word
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(SyllableSplitter(language), first=True)
        syllables_per_word = [len(word._.syllables)
                            for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)
                            for word in doc
                            if not word.is_punct and not word.is_digit and word._.syllables is not None]

        return np.mean(syllables_per_word)


def get_std_of_syllables_per_word(text: str, language: str='es', workers=-1) -> float:
    """
    This function returns the standard deviation of the amount of syllables in each word

    Parameters:
    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed
    workers(int): Amount of threads that will complete this operation. If it's -1 then all cpu cores will be used

    Returns:
    float: The standard deviation of the amount in syllables in each word
    """
    if len(text) == 0:
        raise ValueError('The text is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    elif workers == 0 or workers < -1:
        raise ValueError('Workers must be -1 or any positive number greater than 0')
    else:
        paragraphs = split_text_into_paragraphs(text) # Obtain paragraphs
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        nlp = spacy.load(language, disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(SyllableSplitter(language), first=True)
        syllables_per_word = [len(word._.syllables)
                            for doc in nlp.pipe(paragraphs, batch_size=threads, disable=['parser', 'tagger', 'ner'], n_process=threads)
                            for word in doc
                            if not word.is_punct and not word.is_digit and word._.syllables is not None]

        return np.std(syllables_per_word)
