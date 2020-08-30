import pandas as pd
import time

from src.processing.text_complexity_analizer import TextComplexityAnalizer

from src.processing.coh_metrix_indices.syntactic_complexity_indices import SyntacticComplexityIndices
import spacy

from src.processing.constants import BASE_DIRECTORY
from src.processing.data_handler.models.obtained_text import ObtainedText
from src.processing.data_handler.models.descriptive_index import DescriptiveIndex
from src.processing.data_handler.models.connective_index import ConnectiveIndex
from src.processing.data_handler.models.lexical_diversity_index import LexicalDiversityIndex
from src.processing.data_handler.models.readability_index import ReadabilityIndex
from src.processing.data_handler.models.referential_cohesion_index import ReferentialCohesionIndex
from src.processing.data_handler.models.syntactic_complexity_index import SyntacticComplexityIndex
from src.processing.data_handler.models.syntactic_pattern_density_index import SyntacticPatternDensityIndex
from src.processing.data_handler.models.word_information_index import WordInformationIndex
from src.preparation.obtained_text_da import ObtainedTextDA

def foo(a, b):
    return a + b

if __name__ == "__main__":
    '''documents = ['/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt']
    descriptive = pd.DataFrame(columns=['DESPC', 'DESSC', 'DESWC', 'DESPL', 'DESPLd', 'DESSL', 'DESSLd', 'DESWLsy', 'DESWLsyd', 'DESWLlt', 'DESWLltd'])
    word_information = pd.DataFrame(columns=['WRDNOUN', 'WRDVERB', 'WRDADJ', 'WRDADV', 'WRDPRO', 'WRDPRP1s', 'WRDPRP1p', 'WRDPRP2s', 'WRDPRP2p', 'WRDPRP3s', 'WRDPRP3p'])
    syntactic_pattern_density = pd.DataFrame(columns=['DRNP', 'DRVP', 'DRNEG'])
    syntactic_complexity = pd.DataFrame(columns=['SYNNP'])
    connective = pd.DataFrame(columns=['CNCAll', 'CNCCaus', 'CNCLogic', 'CNCADC', 'CNCTemp', 'CNCAdd'])
    lexical_diversity = pd.DataFrame(columns=['LDTTRa', 'LDTTRcw'])
    readability = pd.DataFrame(columns=['RDFHGL'])
    referential_cohesion = pd.DataFrame()

    try:
        tca = TextComplexityAnalizer('es')
        
        for filepath in documents: # For each file
            with open(filepath, 'r') as f:
                text = f.read()
                start = time.time()
                descriptive_row = tca.calculate_descriptive_indices_for_one_text(text)
                word_count = descriptive_row['DESWC']
                mean_words_per_sentence = descriptive_row['DESSL']
                mean_syllables_per_word = descriptive_row['DESWLsy']
                descriptive = descriptive.append(descriptive_row, ignore_index=True)
                word_information = word_information.append(tca.calculate_word_information_indices_for_one_text(text, word_count), ignore_index=True)
                syntactic_pattern_density = syntactic_pattern_density.append(tca.calculate_syntactic_pattern_density_indices_for_one_text(text, word_count), ignore_index=True)
                syntactic_complexity = syntactic_complexity.append(tca.calculate_syntactic_complexity_indices(text), ignore_index=True)
                connective = connective.append(tca.calculate_connective_indices(text, word_count), ignore_index=True)
                lexical_diversity = lexical_diversity.append(tca.calculate_lexical_diversity_density_indices_for_one_text(text), ignore_index=True)
                readability = readability.append(tca.calculate_readability_indices(text, mean_words_per_sentence=mean_words_per_sentence, mean_syllables_per_word=mean_syllables_per_word), ignore_index=True)
                referential_cohesion = referential_cohesion.append(tca.calculate_referential_cohesion_indices(text=text), ignore_index=True)
                end = time.time()        
                filename = filepath.split('/')[-1]   
                print(f'Tiempo demorado para {filename}: {end - start} segundos.')

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
        print(referential_cohesion)'''
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

    da = ObtainedTextDA()
    texts = da.select_all_as_dataframe()
    print(texts)