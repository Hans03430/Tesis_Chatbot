import asyncio
from src.data_obtaining.pdf_processing import convert_pdf_to_txt

asyncio.run(convert_pdf_to_txt('/home/hans/Documentos/Tesis_Chatbot/data/raw/pdf/1/Historia, Geografía y Economía/atahualpa.pdf', 'atahualpa.txt'))