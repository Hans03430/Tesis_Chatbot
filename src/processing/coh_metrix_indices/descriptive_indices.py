import numpy as np
import string


from spacy.lang.es import Spanish
from spacy.util import get_lang_class
from typing import List


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
    text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
    sentences = split_text_into_sentences(text_without_punctuation, language)
    word_count = 0
    for sentence in sentences:
        word_count += len(split_sentence_into_words(sentence, language))
    
    return word_count


def get_mean_of_length_of_paragraphs(text: str, language: str='es') -> float:
    """
    This function returns the average numbers of sentences in each paragraph

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    float: The mean of the amount in sentences in each paragraph
    """
    paragraphs = split_text_into_paragraphs(text)
    sentences_per_paragraph = np.zeros(len(paragraphs))
    for i in range(len(paragraphs)): # Count the amount of sentences for each paragraph
        sentences_per_paragraph[i] = get_sentence_count_from_text(paragraphs[i], language)
    
    return np.mean(sentences_per_paragraph)

def get_std_of_length_of_paragraphs(text: str, language: str='es') -> float:
    """
    This function returns the standard deviation of the mean of sentences of each paragraph

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    float: The standard deviation of the mean of the amount in sentences in each paragraph
    """
    paragraphs = split_text_into_paragraphs(text)
    sentences_per_paragraph = np.zeros(len(paragraphs))
    for i in range(len(paragraphs)): # Count the amount of sentences for each paragraph
        sentences_per_paragraph[i] = get_sentence_count_from_text(paragraphs[i], language)
    
    return np.std(sentences_per_paragraph)


def get_mean_of_length_of_sentences(text: str, language: str='es') -> float:
    """
    This function returns the average amount of words in each sentence

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    float: The mean of the amount in words in each sentence.
    """
    sentences = split_text_into_sentences(text)
    sentences_per_sentence= np.zeros(len(sentences))
    for i in range(len(sentences)): # Count the amount of sentences for each paragraph
        sentences_per_sentence[i] = get_word_count_from_text(sentences[i], language)
    
    return np.mean(sentences_per_sentence)


def get_std_of_length_of_sentences(text: str, language: str='es') -> float:
    """
    This function returns the standard deviation of the amount of words in each sentence

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    float: The standard deviation of the amount in words in each sentence.
    """
    sentences = split_text_into_sentences(text, language)
    sentences_per_sentence= np.zeros(len(sentences))
    for i in range(len(sentences)): # Count the amount of sentences for each paragraph
        sentences_per_sentence[i] = get_word_count_from_text(sentences[i], language)
    
    return np.std(sentences_per_sentence)


def get_mean_of_length_of_words(text: str, language: str='es') -> float:
    """
    This function returns the average amount of letters in each word

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    float: The mean of the amount in letters in each word
    """
    words = split_sentence_into_words(text)
    letters_per_word = np.zeros(len(words))
    for i in range(len(words)): # Count the amount of sentences for each paragraph
        letters_per_word[i] = len(words[i])
    
    return np.mean(letters_per_word)


def get_std_of_length_of_words(text: str, language: str='es') -> float:
    """
    This function returns the average amount of letters in each word

    text(str): The text to be anaylized
    language(str): The language of the text to be analyzed

    Returns:
    float: The mean of the amount in letters in each word
    """
    words = split_sentence_into_words(text)
    letters_per_word = np.zeros(len(words))
    for i in range(len(words)): # Count the amount of sentences for each paragraph
        letters_per_word[i] = len(words[i])
    
    return np.std(letters_per_word)