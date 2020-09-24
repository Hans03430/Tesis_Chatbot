import asyncio
import re
import spacy
import tika

from aiofile import AIOFile
from src.processing.constants import ACCEPTED_LANGUAGES
from src.processing.utils.utils import split_text_into_paragraphs
from tika import parser


async def convert_pdf_to_txt(pdf_path: str, save_dir: str) -> None:
    """
    This function converts a pdf file to a txt file. It cleans the text.
    
    Parameters:
    pdf_path (str): The path where the pdf to covert is located
    save_dir (str): The path where to save the converted pdf
    
    Returns:
    None
    """
    if not hasattr(convert_pdf_to_txt, 'nlp'):
        convert_pdf_to_txt.nlp = spacy.load(ACCEPTED_LANGUAGES['es'])
        convert_pdf_to_txt.nlp.add_pipe(convert_pdf_to_txt.nlp.create_pipe('sentencizer'))
    try:
        tika.initVM()
        pdf_file = parser.from_file(pdf_path)
        async with AIOFile(save_dir, 'w') as text_file:
            doc = convert_pdf_to_txt.nlp(pdf_file['content'])
            #print(doc)
            text = ''.join([re.sub(r'[,|;|\b]\n+\b', '\n', re.sub(r'\b\n+\b', '\n', s.text))
                            for s in doc.sents]) # Fix sentences that have more newlines than they should
            paragraphs = split_text_into_paragraphs(text) # Eliminate extra newlines between paragraphs
            new_text = '\n\n'.join(paragraphs)
            new_text = re.sub(r'-\s*\n+', '', new_text) # Join split words.
            print(new_text)
            await text_file.write(new_text)

    except Exception as e:
        raise e
