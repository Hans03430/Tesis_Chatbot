import pandas as pd
import time

from src.processing.text_complexity_analizer import TextComplexityAnalizer

from src.processing.coh_metrix_indices.syntactic_complexity_indices import SyntacticComplexityIndices
import spacy

if __name__ == "__main__":
    documents = ['/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/3/CTA/biodiversidad_docente.txt']
    descriptive = pd.DataFrame(columns=['DESPC', 'DESSC', 'DESWC', 'DESPL', 'DESPLd', 'DESSL', 'DESSLd', 'DESWLsy', 'DESWLsyd', 'DESWLlt', 'DESWLltd'])
    word_information = pd.DataFrame(columns=['WRDNOUN', 'WRDVERB', 'WRDADJ', 'WRDADV', 'WRDPRO', 'WRDPRP1s', 'WRDPRP1p', 'WRDPRP2s', 'WRDPRP2p', 'WRDPRP3s', 'WRDPRP3p'])
    syntactic_pattern_density = pd.DataFrame(columns=['DRNP', 'DRVP', 'DRNEG'])
    syntactic_complexity = pd.DataFrame(columns=['SYNNP'])
    connective = pd.DataFrame(columns=['CNCAll', 'CNCCaus', 'CNCLogic', 'CNCADC', 'CNCTemp', 'CNCAdd'])
    lexical_diversity = pd.DataFrame(columns=['LDTTRa', 'LDTTRcw'])
    readability = pd.DataFrame(columns=['RDFHGL'])

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