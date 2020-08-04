import time

from src.processing.text_complexity_analizer import TextComplexityAnalizer

if __name__ == "__main__":
    documents = ['/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt']
    tca = TextComplexityAnalizer('es')
    results = tca.analize_texts(documents)
    print(results)
