import asyncio

from src.data_obtaining.pdf_processing import convert_pdf_to_txt
from src.processing.utils.utils import split_text_into_paragraphs
import re
import spacy

nlp = spacy.load('es_core_news_lg', disable=['parser', 'tagger', 'ner'])
nlp.add_pipe(nlp.create_pipe('sentencizer'))
text = '''
Este es un mensaje de prueba.





¿Hola como están el día   
de hoy?





Este es un día


muy especial para todos nosotros.
Debido a ello, hoy tendremos mucha suerte.





Entonces, lo importante es ganar al otro equipo.
Así, tendremos la ventaja durante todo el año.'''

paragraphs = split_text_into_paragraphs(text)
print(paragraphs)
print('\n\n'.join(paragraphs))