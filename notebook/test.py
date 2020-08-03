import time

import spacy
from src.processing.coh_metrix_indices.descriptive_indices import *
from src.processing.coh_metrix_indices.word_information_indices import *
from src.processing.coh_metrix_indices.synthactic_pattern_density_indices import *

def test_function(function, text):
    start = time.time()
    response = function(text)
    end = time.time()
    print(f'Respuesta: {response}. Tiempo demorado: {end - start}. Function: {function}')

with open('/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt', 'r') as document:
    #text = document.read()
    text = '''Documento de prueba número uno que será usado para probar las funciones.
No se necesita hacer muchas cosas con este documento.

Para mayor información por favor llamar al número que aparece en pantalla.

¿Cómo está el día de hoy?

Yo me encuentro muy bien en este bello día de verano.
Esto se debe a que me encanta el sol


ya que simplemente es hermoso.
1 2 3'''
    '''di = DescriptiveIndices('es')
    test_function(di.get_paragraph_count_from_text, text)
    test_function(di.get_sentence_count_from_text, text)
    test_function(di.get_word_count_from_text, text)
    test_function(di.get_mean_of_length_of_paragraphs, text)
    test_function(di.get_std_of_length_of_paragraphs, text)
    test_function(di.get_mean_of_length_of_sentences, text)
    test_function(di.get_std_of_length_of_sentences, text)
    test_function(di.get_mean_of_length_of_words, text)
    test_function(di.get_std_of_length_of_words, text)
    test_function(di.get_mean_of_syllables_per_word, text)
    test_function(di.get_std_of_syllables_per_word, text)'''

    nlp = spacy.load('es', disable=['tagger', 'parser', 'ner'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    text_spacy = nlp(text)
    omg = []
    for sentence in text_spacy.sents:
        omg.append(sentence)
        print(sentence)

    print(len(omg))
