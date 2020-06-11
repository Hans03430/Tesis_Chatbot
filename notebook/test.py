import spacy
from src.processing.coh_metrix_indices.descriptive_indices import *
from src.processing.coh_metrix_indices.word_information_indices import *
text = '''
Joaquín Baldomero Fernández-Espartero Álvarez de Toro (Granátula de Calatrava, Ciudad Real, 27 de febrero de 1793-Logroño, 8 de enero de 1879) fue virrey de Navarra, príncipe de Vergara, duque de la Victoria, duque de Morella, conde de Luchana y vizconde de Banderas, títulos concedidos por su carrera como general y regente de España.

Su padre había encauzado su formación para un destino eclesiástico pero la Guerra de la Independencia lo arrastró desde muy joven al frente de batalla, que no abandonó hasta veinticinco años después. Combatiente en tres de los cuatro conflictos más importantes de España en el siglo xix, fue soldado en la guerra contra la invasión francesa, oficial durante la guerra colonial en el Perú y general en jefe en la guerra civil. Vivió en Cádiz el nacimiento del liberalismo español, senda que no abandonaría jamás. Hombre extremadamente duro en el trato, valoraba la lealtad de sus compañeros de armas —término que no gustaban de oír los demás generales— tanto como la eficacia. Combatió en primera línea, fue herido en ocho ocasiones y su carácter altivo y exigente lo llevó a cometer excesos, en ocasiones muy sangrientos, en la disciplina militar. Convencido de que su destino era gobernar a los españoles, fue por dos veces presidente del Consejo de Ministros y llegó a la jefatura del Estado como regente durante la minoría de edad de Isabel II. Ha sido el único militar español con tratamiento de Alteza Real y, a pesar de todas sus contradicciones, supo pasar desapercibido los últimos veintiocho años. Rechazó la Corona de España y fue tratado como una leyenda desde bien joven.
'''

sentences = split_text_into_sentences(text, 'es')
for x in sentences:
    print(x)

for x in split_sentence_into_words(sentences[0], 'es'):
    print(x)

results = get_word_grammatical_information(text, 'es')
print(results)