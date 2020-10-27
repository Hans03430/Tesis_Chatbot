'''
This module contains generic functions to reutilze across the "preparation" module.
'''
import re
import spacy

from aiofile import AIOFile

async def obtain_text_file_as_string(file_path: str) -> str:
    """
    This function reads a text file from the given path and returns it as a string

    Parameters:
    file_path(str): The path where the file is located

    Returns:
    str: The file as a string
    """
    async with AIOFile(file_path, 'r') as text_file:
        text_string = await text_file.read()
        return text_string

def clean_string(text: str) -> str:
    '''
    This function cleans a string.
    
    Parameters:
    text(str): The string to clean.

    Returns:
    str: The cleaned string.
    '''
    if not hasattr(clean_string, 'nlp'): # To clean stop words
        print('Creating nlp model.')
        clean_string.nlp = spacy.load('es_core_news_lg', disable=['parser', 'tagger', 'ner'])

    doc = clean_string.nlp(text)
    joined =  ' '.join([token.text
                        for token in doc
                        if token.is_alpha and not token.is_stop
                    ])
    clean = re.sub(r'[^\w\s]', ' ', joined).strip()
    clean = re.sub(r'\s\s*', ' ', clean)
    return clean