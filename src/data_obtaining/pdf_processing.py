import asyncio
import tika
from tika import parser
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
        tika.initVM()
        pdf_file = parser.from_file(pdf_path)
        async with AIOFile(save_dir, 'w') as text_file:
            await text_file.write(pdf_file['content'])

    except Exception as e:
        raise e
