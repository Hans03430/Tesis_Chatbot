import asyncio
import pdftotext

from aiofile import AIOFile


async def convert_pdf_to_txt(pdf_path: str, save_dir: str) -> None:
    """
    This function converts a pdf file to a txt file
    
    Parameters:
    pdf_path (str): The path where the pdf to covert is located
    save_dir (str): The path where to save the converted pdf
    
    Returns:
    None
    """
    try:
        with open(pdf_path, mode='rb') as pdf_file:
            pdf_reader = pdftotext.PDF(pdf_file)
            text = ''.join(pdf_reader)

            async with AIOFile(save_dir, 'w') as text_file:
                await text_file.write(text)

    except Exception as e:
        raise e
