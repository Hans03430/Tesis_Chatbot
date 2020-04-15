import io

import asyncio
import PyPDF2

from aiofile import AIOFile


async def convert_pdf_to_txt(pdf_path: str, save_dir: str) -> None:
    """
    This function converts a pdf file to a txt file
    Adapted from: https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    
    Parameters:
    pdf_path (str): The path where the pdf to covert is located
    save_dir (str): The path where to save the converted pdf
    
    Returns:
    None
    """
    try:
        with open(pdf_path, mode='rb') as pdf_file:
            reader = PyPDF2.PdfFileReader(pdf_file)
            text = ''.join([page.extractText() for page in reader.pages])
            
            async with AIOFile(save_dir, 'w') as text_file:
                await text_file.write(text)

    except Exception as e:
        raise e
