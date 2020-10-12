'''
This module contains generic functions to reutilze across the "preparation" module.
'''
import re

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

def clean_string_from_punctuation(text: str) -> str:
    '''
    This function removes punctuation from a string.
    
    Parameters:
    text(str): The string to clean.

    Returns:
    str: The cleaned string.
    '''
    return re.sub(r'[^\w\s]', ' ', text)