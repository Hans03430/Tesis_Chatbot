import multiprocessing
import numpy as np
import string

from itertools import chain
from itertools import repeat
from spacy.lang.es import Spanish
from spacy.util import get_lang_class
from typing import List

from src.processing.constants import ACCEPTED_LANGUAGES

def split_text_into_paragraphs(text: str) -> List[str]:
    """
    This function splits a text into paragraphs. It assumes paragraphs are separated by two line breaks

    Parameters:
    text(str): The text to be split into paragraphs

    Returns:
    List[str]: A list of paragraphs
    """
    return text.split('\n\n')
    

def split_text_into_sentences(text: str, language: str='es') -> List[str]:
    """
    This function splits a text into sentences

    Parameters:
    text(str): The text to be split into sentences

    Returns:
    List[str]: A list of sentences
    """
    if not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    cls = get_lang_class(language)
    nlp = cls()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    text_spacy = nlp(text)
    return [str(sentence) for sentence in text_spacy.sents]


def split_sentence_into_words(sentence:str, language: str='es') -> List[str]:
    """
    This function splits a sentence into words

    Parameters:
    sentence(str): The sentence to be split
    """
    if not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')
    cls = get_lang_class(language)
    nlp = cls()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    sentence_spacy = nlp(sentence)
    return [str(token.text) for token in sentence_spacy]


def get_paragraph_count_from_text(text: str) -> int:
    """
    This function counts how many paragarphs are there in a text

    Parameters:
    text(str): The text to be analyzed

    Returns:
    int: The amount of paragraphs in a text
    """
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
    if not language in ACCEPTED_LANGUAGES:
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
    if not language in ACCEPTED_LANGUAGES:
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
    elif workers == 1:
        sentences_per_paragraph = np.array([get_sentence_count_from_text(paragraph, language) for paragraph in paragraphs])

        return np.mean(sentences_per_paragraph)
    else:
        paragraphs = split_text_into_paragraphs(text)
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        pool = multiprocessing.Pool(threads)
        sentences_per_paragraph_batches = pool.starmap(get_sentence_count_from_text, zip(paragraphs, repeat(language)))
        pool.close()
        pool.join()
        return np.mean(np.array(sentences_per_paragraph_batches))

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
    elif workers == 1:
        sentences_per_paragraph = np.array([get_sentence_count_from_text(paragraph, language) for paragraph in paragraphs])

        return np.std(sentences_per_paragraph)
    else:
        paragraphs = split_text_into_paragraphs(text)
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        pool = multiprocessing.Pool(threads)
        sentences_per_paragraph_batches = pool.starmap(get_sentence_count_from_text, zip(paragraphs, repeat(language)))
        pool.close()
        pool.join()
        return np.std(np.array(sentences_per_paragraph_batches))


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
    elif workers == 1:
        sentences = split_text_into_sentences(text)
        words_per_sentence = np.array([get_word_count_from_text(sentence, language) for sentence in sentences])
        
        return np.mean(words_per_sentence)
    else:
        sentences = split_text_into_sentences(text)
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        pool = multiprocessing.Pool(threads)
        words_per_sentence_batches = pool.starmap(get_word_count_from_text, zip(sentences, repeat(language)))
        pool.close()
        pool.join()
        return np.mean(np.array(words_per_sentence_batches))


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
    elif workers == 1:
        sentences = split_text_into_sentences(text)
        words_per_sentence = np.array([get_word_count_from_text(sentence, language) for sentence in sentences])
        
        return np.std(words_per_sentence)
    else:
        sentences = split_text_into_sentences(text)
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        pool = multiprocessing.Pool(threads)
        words_per_sentence_batches = pool.starmap(get_word_count_from_text, zip(sentences, repeat(language)))
        pool.close()
        pool.join()
        return np.std(np.array(words_per_sentence_batches))


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
    elif workers == 1:
        words = split_sentence_into_words(text)
        letters_per_word = np.array([len(word) for word in words])

        return np.mean(letters_per_word)
    else:
        words = split_sentence_into_words(text)
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        pool = multiprocessing.Pool(threads)
        letters_per_word_batches = pool.map(len, words)
        pool.close()
        pool.join()
        return np.mean(np.array(letters_per_word_batches))


def get_std_of_length_of_words(text: str, language: str='es', workers=-1) -> float:
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
    elif workers == 1:
        words = split_sentence_into_words(text)
        letters_per_word = np.array([len(word) for word in words])

        return np.std(letters_per_word)
    else:
        words = split_sentence_into_words(text)
        threads = multiprocessing.cpu_count() if workers == -1 else workers
        pool = multiprocessing.Pool(threads)
        letters_per_word_batches = pool.map(len, words)
        pool.close()
        pool.join()
        return np.std(np.array(letters_per_word_batches))