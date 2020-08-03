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
    text = '''Él le dijo a ella que ustedes no vendrían a clases aquel día.
Esto se debe a que usted nunca nos dijo nada a nosotros.

Ahora yo no se que hacer debido a que ellas no vendrán a la reunión.'''
    di = DescriptiveIndices('es')
    wi = WordInformationIndices('es')
    test_function(wi.get_noun_count, text)
    test_function(wi.get_verb_count, text)
    test_function(wi.get_adjective_count, text)
    test_function(wi.get_adverb_count, text)
    test_function(wi.get_personal_pronoun_count, text)
    test_function(wi.get_personal_pronoun_first_person_single_form_count, text)
    test_function(wi.get_personal_pronoun_first_person_plural_form_count, text)
    test_function(wi.get_personal_pronoun_second_person_single_form_count, text)
    test_function(wi.get_personal_pronoun_second_person_plural_form_count, text)
    test_function(wi.get_personal_pronoun_third_person_singular_form_count, text)
    test_function(wi.get_personal_pronoun_third_person_plural_form_count, text)
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
    test_function(di.get_std_of_syllables_per_word, text)

    '''nlp = spacy.load('es', disable=['tagger', 'parser', 'ner'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    text_spacy = nlp(text)
    omg = []
    for sentence in text_spacy.sents:
        omg.append(sentence)
        print(sentence)

    print(len(omg))'''
