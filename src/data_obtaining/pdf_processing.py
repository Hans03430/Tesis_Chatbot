import asyncio
import re
import tika

from aiofile import AIOFile
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
    try:
        tika.initVM()
        pdf_file = parser.from_file(pdf_path)
        async with AIOFile(save_dir, 'w') as text_file:
            paragraphs = split_text_into_paragraphs(pdf_file['content'])
            new_text = '\n\n'.join(paragraphs)
            new_text = re.sub(r'-\n+', '', new_text)
            await text_file.write(new_text)

    except Exception as e:
        raise e
