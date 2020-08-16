import time

from src.processing.text_complexity_analizer import TextComplexityAnalizer

from src.processing.coh_metrix_indices.syntactic_complexity_indices import SyntacticComplexityIndices
from src.processing.coh_metrix_indices.connective_indices import ConnectiveIndices
import spacy

if __name__ == "__main__":
    documents = ['/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt']
    tca = TextComplexityAnalizer('es')
    results = tca.analize_texts(documents)
    print(results)
    '''with open('/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt', 'r') as f:
        ci = ConnectiveIndices('es')
        text = f.read()
        start = time.time()
        print(ci.get_causal_connectives_incidence(text))
        print(ci.get_logical_connectives_incidence(text))
        print(ci.get_adversative_connectives_incidence(text))
        print(ci.get_temporal_connectives_incidence(text))
        print(ci.get_additive_connectives_incidence(text))
        print(ci.get_all_connectives_incidence(text))
        end = time.time()
        print(f'Demoró {end - start} segundos.')'''