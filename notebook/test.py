import time

import spacy
from spacy import displacy
from src.processing.coh_metrix_indices.descriptive_indices import *
from src.processing.coh_metrix_indices.word_information_indices import *
from src.processing.coh_metrix_indices.synthactic_pattern_density_indices import *
from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger

def test_function(function, text):
    start = time.time()
    response = function(text)
    end = time.time()
    print(f'Respuesta: {response}. Tiempo demorado: {end - start}. Function: {function}')

with open('/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt', 'r') as document:
    #text = document.read()
    text = '''El partido está a punto de empezar.
Voy a estudiar el examen de la semana que viene.
Tengo estudiado.
Llevo estudiado.
Luego de llevar leído por muchas horas, pude descansar.
'''
    '''di = DescriptiveIndices('es')
    wi = WordInformationIndices('es')
    spdi = SynthacticPatternDensityIndices('es')
    test_function(spdi.get_noun_phrase_density, text)
    test_function(spdi.get_verb_phrase_density, text)
    test_function(spdi.get_negative_expressions_density, text)
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
    test_function(di.get_std_of_syllables_per_word, text)'''

    nlp = spacy.load('es')
    #nlp.add_pipe(nlp.create_pipe('sentencizer'))
    nlp.add_pipe(VerbPhraseTagger(nlp, 'es'))
    doc = nlp(text)

    for vp in doc._.verb_phrases:
        print(vp)

    for token in doc:
        print(token, token.pos_, token.tag_, token.dep_)

    displacy.serve(doc, style='dep')

