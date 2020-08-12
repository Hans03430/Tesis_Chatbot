import time

from src.processing.text_complexity_analizer import TextComplexityAnalizer

from src.processing.coh_metrix_indices.syntactic_complexity_indices import SyntacticComplexityIndices

import spacy

if __name__ == "__main__":
    documents = ['/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt']
    tca = TextComplexityAnalizer('es')
    results = tca.analize_texts(documents)
    print(results)
