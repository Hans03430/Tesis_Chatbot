import pandas as pd
import time

from src.processing.text_complexity_analyzer import TextComplexityAnalyzer

from src.processing.coh_metrix_indices.syntactic_complexity_indices import SyntacticComplexityIndices
import spacy

from src.processing.constants import BASE_DIRECTORY

def foo(a, b):
    return a + b

if __name__ == "__main__":
    ''#documents = ['/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt']
    descriptive = pd.DataFrame(columns=['DESPC', 'DESSC', 'DESWC', 'DESPL', 'DESPLd', 'DESSL', 'DESSLd', 'DESWLsy', 'DESWLsyd', 'DESWLlt', 'DESWLltd'])
    word_information = pd.DataFrame(columns=['WRDNOUN', 'WRDVERB', 'WRDADJ', 'WRDADV', 'WRDPRO', 'WRDPRP1s', 'WRDPRP1p', 'WRDPRP2s', 'WRDPRP2p', 'WRDPRP3s', 'WRDPRP3p'])
    syntactic_pattern_density = pd.DataFrame(columns=['DRNP', 'DRVP', 'DRNEG'])
    syntactic_complexity = pd.DataFrame(columns=['SYNNP'])
    connective = pd.DataFrame(columns=['CNCAll', 'CNCCaus', 'CNCLogic', 'CNCADC', 'CNCTemp', 'CNCAdd'])
    lexical_diversity = pd.DataFrame(columns=['LDTTRa', 'LDTTRcw'])
    readability = pd.DataFrame(columns=['RDFHGL'])
    referential_cohesion = pd.DataFrame()

    try:
        tca = TextComplexityAnalyzer('es')


        text = '''Ellos jugaron todo el día. Asimismo, ellas participaron en el juego.


Yo corro con el hermoso gato. A nosotros no nos gusta el gato.
Ella tiene mascotas. Además, ella tiene plantas y él no.

Tú jamás dijiste que no, porque ustedes debieron salir temprano en la mañana.
'''
        #with open('/home/hans/Documentos/Tesis_Chatbot/data/raw/txt.bak/2/Arte/orientaciones-ensenanza-arte-cultura.txt', 'r') as f:
            #text = f.read()
            
        start = time.time()
        descriptive_row = tca.calculate_descriptive_indices_for_one_text(text.strip())
        word_count = descriptive_row['DESWC']
        mean_words_per_sentence = descriptive_row['DESSL']
        mean_syllables_per_word = descriptive_row['DESWLsy']
        descriptive = descriptive.append(descriptive_row, ignore_index=True)
        word_information = word_information.append(tca.calculate_word_information_indices_for_one_text(text=text, word_count=word_count), ignore_index=True)
        syntactic_pattern_density = syntactic_pattern_density.append(tca.calculate_syntactic_pattern_density_indices_for_one_text(text=text, word_count=word_count), ignore_index=True)
        syntactic_complexity = syntactic_complexity.append(tca.calculate_syntactic_complexity_indices_for_one_text(text=text), ignore_index=True)
        connective = connective.append(tca.calculate_connective_indices_for_one_text(text=text, word_count=word_count), ignore_index=True)
        lexical_diversity = lexical_diversity.append(tca.calculate_lexical_diversity_density_indices_for_one_text(text=text), ignore_index=True)
        readability = readability.append(tca.calculate_readability_indices_for_one_text(text, mean_words_per_sentence=mean_words_per_sentence, mean_syllables_per_word=mean_syllables_per_word), ignore_index=True)
        referential_cohesion = referential_cohesion.append(tca.calculate_referential_cohesion_indices_for_one_text(text=text), ignore_index=True)
        end = time.time()  
        #print(f"Tiempo demorado: {end - start} segundos.")
                #filename = filepath.split('/')[-1]   
                #print(f'Tiempo demorado para {filename}: {end - start} segundos.')

    except Exception as e:
        raise e
    finally:
        print(descriptive)
        print(word_information)
        print(syntactic_pattern_density)
        print(syntactic_complexity)
        print(connective)
        print(lexical_diversity)
        print(readability)
        print(referential_cohesion)

    '''da = ObtainedTextDA()
    print(BASE_DIRECTORY)
    ot = ObtainedText(text='Prueba 3', grade=1, filename='omg.txt')
    #di = DescriptiveIndex()
    #ot.descriptive_index = dz
    da.insert(ot)'''
    '''to_update = da.select_all()[-1]
    #to_update.text = 'OMG'
    to_update.descriptive_index = DescriptiveIndex(DESSC=64.0003)
    da.update(to_update)'''

    '''dic = {'a': 2, 'b': 3}
    print(foo(**dic))

    try:
        tca = TextComplexityAnalizer('es')
        da = ObtainedTextDA()
        obtained_texts = da.select_all()
        
        for ot in obtained_texts:
            start = time.time()
            descriptive_row = tca.calculate_descriptive_indices_for_one_text(ot.text)
            word_count = descriptive_row['DESWC']
            mean_words_per_sentence = descriptive_row['DESSL']
            mean_syllables_per_word = descriptive_row['DESWLsy']
            ot.descriptive_index = DescriptiveIndex(**descriptive_row)
            ot.word_information_index = WordInformationIndex(**tca.calculate_word_information_indices_for_one_text(ot.text, word_count))
            ot.syntactic_pattern_density_index = SyntacticPatternDensityIndex(**tca.calculate_syntactic_pattern_density_indices_for_one_text(ot.text, word_count))
            ot.syntactic_complexity_index = SyntacticComplexityIndex(**tca.calculate_syntactic_complexity_indices_for_one_text(ot.text))
            ot.connective_index = ConnectiveIndex(**tca.calculate_connective_indices_for_one_text(ot.text, word_count))
            ot.lexical_diversity_index = LexicalDiversityIndex(**tca.calculate_lexical_diversity_density_indices_for_one_text(ot.text))
            ot.readability_index = ReadabilityIndex(**tca.calculate_readability_indices_for_one_text(ot.text, mean_words_per_sentence=mean_words_per_sentence, mean_syllables_per_word=mean_syllables_per_word))
            ot.referential_cohesion_index = ReferentialCohesionIndex(**tca.calculate_referential_cohesion_indices_for_one_text(text=ot.text))
            end = time.time()
            da.update(ot) # Save the indices for the current record       
            print(f'Tiempo demorado para {ot.filename}: {end - start} segundos.')

    except Exception as e:
        raise e'''

    '''da = ObtainedTextDA()
    texts = da.select_all_as_dataframe()
    print(texts)'''