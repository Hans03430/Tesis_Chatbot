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
        
        #for filepath in documents: # For each file
            #with open(filepath, 'r') as f:
                #text = f.read()
#        text = '''Mi prima perdió su celular pero le compraron
#uno nuevo.

#El celular pertenece a la última generación. No obstante,
#a ella no le gusta debido a que es muy grande.

#Ahora mi prima deberá conseguir un celular más pequeño.
#'''
        text = '''Johann Sebastian Bach nació en Eisenach, en el Ducado de Sajonia-Eisenach (en la actual Turingia, Alemania), el 21 de marzo de 1685, el mismo año que Georg Friedrich Händel y Domenico Scarlatti. La fecha de su nacimiento corresponde al calendario juliano, pues los alemanes aún no habían adoptado el calendario gregoriano, por el cual la fecha corresponde al 31 de marzo. Fue el octavo hijo (el hijo mayor tenía 14 años cuando Johann Sebastian nació)​ del matrimonio formado entre Maria Elisabetha Lämmerhirt y Johann Ambrosius Bach, director de los músicos de la ciudad.5​ Su padre fue quien probablemente le enseñó a tocar el violín y los fundamentos de la teoría musical.6 Su tío Johann Christoph Bach lo introdujo en la práctica del órgano.

Su madre falleció en 1694, cuando Johann Sebastian tenía nueve años, y su padre —que ya le había dado las primeras lecciones de música— falleció ocho meses después.​ Johann Sebastian, huérfano con diez años, se fue a vivir y estudiar con su hermano mayor, Johann Christoph Bach, organista en la iglesia de San Miguel (Michaeliskirche) de Ohrdruf, una ciudad cercana.8 Allí copiaba, estudiaba e interpretaba música, incluyendo la de su propio hermano, a pesar de estar prohibido hacerlo porque las partituras eran muy valiosas y privadas y el papel de ese tipo era costoso.9​ Aprendió teoría musical y composición, además de tocar el órgano, y recibió lecciones de su hermano, que lo adiestró en la interpretación del clavicordio. Johann Christoph le dio a conocer las obras de los grandes compositores del Sur de Alemania de la época, como Johann Pachelbel (que había sido maestro de Johann Christoph)1 y Johann Jakob Froberger; de compositores del Norte de Alemania;​ de los franceses, como Jean-Baptiste Lully, Louis Marchand y Marin Marais, así como del clavecinista italiano Girolamo Frescobaldi. También en esa época estudió teología, latín, griego, francés e italiano en el gymnasium de la localidad.1
Registro escolar del Liceo de Ohrdruf. J. S. Bach es el cuarto alumno de la segunda lista.

En 1700, a sus catorce años de edad, Johann Sebastian fue premiado, junto a su amigo del colegio Georg Erdmann, dos años mayor que él, con una matrícula para realizar estudios corales en la prestigiosa Escuela de San Miguel en Luneburgo, no muy lejos del puerto marítimo de Hamburgo, una de las ciudades más grandes del Sacro Imperio Romano. Esto conllevaba un largo viaje con su amigo, que probablemente realizaron en parte a pie y en parte en carroza, aunque no se sabe con certeza.13​ No hay referencias escritas de este período de su vida, pero los dos años de estancia en la escuela parecen haber sido decisivos, por haberle expuesto a una paleta más amplia de la cultura europea que la que había experimentado en Turingia. Además de cantar en el coro a capella, es probable que tocase el órgano con tres teclados y sus clavicémbalos. Quizás entró en contacto con los hijos de los nobles del Norte de Alemania, que eran enviados a esta escuela selectísima para prepararse en sus carreras diplomáticas, gubernamentales y militares.

Aunque existen pocas evidencias históricas que lo sustenten, es casi seguro que durante la estancia en Luneburgo, el joven Bach visitó la iglesia de San Juan (Johanniskirche) y escuchó (y posiblemente tocó) el famoso órgano de la iglesia (construido en 1549 por Jasper Johannsen, y conocido como «el órgano de Böhm» debido a su intérprete más destacado). Dado su talento musical, es muy probable asimismo que tuviese un significativo contacto con los organistas destacados del momento en Luneburgo, muy particularmente con Georg Böhm (el organista de la Johanniskirche), así como con organistas de la cercana Hamburgo, como Johann Adam Reincken y Nicolaus Bruhns. Gracias al contacto con estos músicos, Johann Sebastian tuvo acceso probablemente a los instrumentos más grandes y precisos que había tocado hasta entonces. En esta etapa se familiarizó con la música de la tradición académica organística del Norte de Alemania, especialmente con la obra de Dietrich Buxtehude, organista en la iglesia de Santa María de Lübeck, y con manuscritos musicales y tratados de teoría musical que estaban en posesión de aquellos músicos.Stauffer informó del descubrimiento en 2005 de las tablaturas de órganos que Bach escribió, aun en su adolescencia, de obras de Reincken y Dieterich Buxtehude, que muestra «un adolescente disciplinado, metódico y bien entrenado profundamente comprometido con el aprendizaje de su oficio».

En enero de 1703, poco después de terminar los estudios y graduarse en San Miguel y de ser rechazado para el puesto de organista en Sangerhausen, Bach logró un puesto como músico de la corte en la capilla del duque Juan Ernesto III, en Weimar.​ No está claro cuál fue su papel allí, pero parece que incluía tareas domésticas no musicales. Durante sus siete meses de servicio en Weimar, su reputación como teclista se extendió tanto que fue invitado a inspeccionar el flamante órgano de la iglesia de San Bonifacio (St.-Bonifatius-Kirche, posteriormente Bachkirche, iglesia de Bach) de la cercana ciudad de Arnstadt, a 40 kilómetros al sureste de Weimar, y a dar el concierto inaugural en él. La familia Bach tenía estrechos vínculos con esta vieja ciudad de Turingia, al lado del bosque de Turingia. En agosto de 1703, aceptó el puesto de organista en dicha iglesia, con obligaciones ligeras, un salario relativamente generoso y un buen órgano nuevo, afinado conforme a un sistema nuevo que permitía que se utilizara un mayor número de teclas. En esa época, Bach estaba emprendiendo la composición seria de preludios para órgano; estas obras, inscritas en la tradición del Norte de Alemania de preludios virtuosos e improvisatorios, ya mostraban un estricto control de los motivos (en ellos, una idea musical sencilla y breve se explora en sus consecuencias a través de todo un movimiento). Sin embargo, en estas obras el compositor aún no había desarrollado plenamente su capacidad de organización a gran escala y su técnica contrapuntística, donde dos o más melodías interactúan simultáneamente.

A pesar de las fuertes conexiones familiares y el hecho de estar empleado por un entusiasta de la música no impidieron que surgiera tensión entre el joven organista y las autoridades después de varios años en el puesto. Johann Sebastian estaba insatisfecho con el nivel de los cantantes del coro. Llamó a uno de ellos «Zippel Fagottist» (fagotista flojo). Una noche, este estudiante llamado Geyersbach fue tras él con un palo. Bach presentó una denuncia contra él ante las autoridades. Absolvieron a Geyersbach con una pequeña reprimenda y ordenaron a Bach que fuera más moderado con respecto a las cualidades musicales que esperaba de sus alumnos. Meses después, su empleador se mostró muy molesto después de que Bach se ausentara de Arnstadt sin autorización durante cuatro meses (había pedido permiso para ausentarse cuatro semanas) en el invierno de 1705-1706 para visitar en Lübeck al gran maestro Dietrich Buxtehude y asistir a sus Abendmusiken en la iglesia de Santa María (Marienkirche). Este episodio bien conocido de la vida del compositor implica que tuvo que caminar unos 400 kilómetros de ida y otros tantos de vuelta a pie para pasar tiempo con el hombre al que posiblemente consideraba como la figura máxima entre los organistas alemanes. El viaje reforzó el influjo del estilo de Buxtehude como fundamento de la obra temprana de Bach y el hecho de que alargase su visita durante varios meses sugiere que el tiempo que pasó con el anciano tuvo un alto valor para su arte. Johann Sebastian quería convertirse en amanuense (asistente o sucesor) de Buxtehude, pero no quiso casarse con su hija, que era la condición para su nombramiento.

En 1706, le ofrecieron un puesto mejor pagado como organista en la iglesia de San Blas (Divi-Blasii-Kirche) de Mühlhausen una importante ciudad al norte.​ El año siguiente tomó posesión de este mejor puesto, con paga y condiciones significativamente superiores, incluyendo un buen coro. A los cuatro meses de haber llegado a Mühlhausen, se casó, el 17 de octubre de 1707, con Maria Barbara Bach, una prima suya en segundo grado, con quien tendría siete hijos, de los cuales cuatro alcanzaron la edad adulta.​ Dos de ellos —Wilhelm Friedemann y Carl Philipp Emanuel—​ llegaron a ser compositores importantes en el ornamentado estilo galante que siguió al barroco. 

El ayuntamiento de la ciudad aceptó los requerimientos de Bach e invirtió una gran suma en la renovación del órgano de la iglesia de San Blas. En 1708, Johann Sebastian escribió la cantata festiva Gott ist mein König, BWV 71 para la inauguración del nuevo concejo de la ciudad, cuya publicación fue costeada por el ayuntamiento. En dos ocasiones, en años posteriores, el compositor tuvo que regresar para dirigirla.

Transcurrido apenas un año, en 1708, le llegó una nueva oferta de trabajo como organista desde la corte ducal en Weimar, por lo que abandonó su puesto en Mühlhausen. Allí, tuvo la oportunidad de trabajar con un contingente grande y bien financiado de músicos profesionales.​ Bach se trasladó con su familia a un apartamento muy cercano al palacio ducal. Ese mismo año nació su primera hija, Catharina Dorothea. Se fue a vivir con ellos la hermana mayor y soltera de Maria Barbara, que permaneció con ellos ayudando en las tareas domésticas hasta su muerte en 1729. También nacieron tres hijos en Weimar: Wilhelm Friedemann, Carl Philipp Emanuel y Johann Gottfried Bernhard. Tuvieron tres hijos más, que sin embargo no vivieron hasta su primer cumpleaños, incluidos los gemelos nacidos en 1713.

Este período en la vida de Bach fue fructífero y comenzó una época de composición de obras para teclado y orquestales. Alcanzó el nivel de competencia y confianza para ampliar las estructuras existentes e incluir influencias del exterior. A la muerte del príncipe Juan Ernesto en 1707, su hermano Guillermo Ernesto había asumido el poder de facto. Por su anterior cercanía con el duque Juan Ernesto, que había sido a su vez un avezado músico y admirador de la música italiana, Bach había estudiado y transcrito las obras de Antonio Vivaldi, Arcangelo Corelli y Giuseppe Torelli, entre otros autores italianos, gracias a lo cual había aprendido a escribir aperturas dramáticas y a emplear los ritmos dinámicos y los esquemas armónicos que se encontraban en dicha música, asimilando su dinamismo y emotividad armónica, y aplicando dichas cualidades a sus propias composiciones, que a su vez eran interpretadas por el conjunto musical del duque Guillermo Ernesto. Absorbió estos aspectos estilísticos en parte mediante la transcripción de conciertos para cuerda y viento para clavecín y órgano de Vivaldi; muchas de esas obras transcritas son todavía interpretadas con frecuencia. Se sintió atraído especialmente con el estilo italiano en el que uno o más instrumentos solistas alternan sección por sección con la orquesta completa a través de un movimiento.

Continuó tocando y componiendo para órgano e interpretando música de concierto con el conjunto del duque.También comenzó a componer preludios y fugas, posteriormente recopilados en su obra monumental El clave bien temperado (Das Wohltemperierte Klavier), impreso por primera vez en 1801, que consta de dos libros compilados en 1722 y 1744, cada uno de los cuales contiene un preludio y fuga en cada tonalidad mayor y menor. Comenzó a escribir Orgelbüchlein (Pequeño libro para órgano) obra didáctica que dejó inconclusa. Contenía corales tradicionales luteranas arregladas en elaboraciones complejas, para formar organistas.

En 1713, le ofrecieron un puesto en Halle cuando aconsejó a las autoridades durante la renovación de Christoph Cuntzius del órgano principal de la galería oeste de la Marktkirche Unser Lieben Frauen.​ Johann Kuhnau y Bach volvieron a tocar cuando se inauguró en 1716.​ En la primavera de 1714, Johann Sebastian fue ascendido a Konzertmeister, un honor que implicaba realizar una cantata de iglesia mensualmente en la iglesia del castillo.​ Las tres primeras cantatas de la nueva serie compuesta por Bach en Weimar fueron Himmelskönig, sei willkommen, BWV 182, para el Domingo de Ramos, que coincidió con la Anunciación de ese año; Weinen, Klagen, Sorgen, Zagen, BWV 12, para el Domingo de júbilo; y Erschallet, ihr Lieder, erklinget, ihr Saiten!, BWV 172 para Pentecostés.​ Su primera cantata navideña, Christen, ätzet diesen Tag, BWV 63, se estrenó aquí posiblemente en 1713. o si fue interpretada para el bicentenario de la Reforma Protestante en 1717.

En 1717, ocurre en Dresde el anecdótico intento de duelo musical con Louis Marchand (se dice que Marchand abandonó la ciudad tras escuchar previamente y a escondidas a Bach). Ese mismo año, con motivo del fallecimiento del maestro de capilla (o Kapellmeister) de la corte de Anhalt-Köthen y con la mediación del duque Ernesto Augusto, el príncipe Leopoldo ofreció a Bach el puesto vacante, que aceptó. Esto disgustó al duque de Weimar y cuando el compositor presentó su renuncia ordenó su arresto por algunas semanas en el castillo antes de aceptarla. Según una traducción del informe del secretario del tribunal, fue encarcelado durante casi un mes antes de ser despedido desfavorablemente: 
'''
        text = '''Yo hago mis tareas todos los días.
Nosotros conocemos unos buenos alumnos.

Él y su familia irán de paseo mañana.
Por otro lado, ella sacará a pasear a su hermoso perro negro.

Ellos jugarán baloncesto con ellas toda la semana.
Tú me debes mucho dinero y ustedes no lo saben.'''
        #with open('/home/hans/Documentos/Tesis_Chatbot/data/raw/txt.bak/2/Arte/orientaciones-ensenanza-arte-cultura.txt', 'r') as f:
            #text = f.read()
            
        start = time.time()
        #descriptive_row = tca.calculate_descriptive_indices_for_one_text(text)
        #word_count = descriptive_row['DESWC']
        #mean_words_per_sentence = descriptive_row['DESSL']
        #mean_syllables_per_word = descriptive_row['DESWLsy']
        #descriptive = descriptive.append(descriptive_row, ignore_index=True)
        #word_information = word_information.append(tca.calculate_word_information_indices_for_one_text(text=text, word_count=word_count), ignore_index=True)
        #syntactic_pattern_density = syntactic_pattern_density.append(tca.calculate_syntactic_pattern_density_indices_for_one_text(text=text, word_count=word_count), ignore_index=True)
        syntactic_complexity = syntactic_complexity.append(tca.calculate_syntactic_complexity_indices_for_one_text(text=text), ignore_index=True)
        #connective = connective.append(tca.calculate_connective_indices_for_one_text(text=text, word_count=word_count), ignore_index=True)
        #lexical_diversity = lexical_diversity.append(tca.calculate_lexical_diversity_density_indices_for_one_text(text=text), ignore_index=True)
        #readability = readability.append(tca.calculate_readability_indices_for_one_text(text, mean_words_per_sentence=mean_words_per_sentence, mean_syllables_per_word=mean_syllables_per_word), ignore_index=True)
        #referential_cohesion = referential_cohesion.append(tca.calculate_referential_cohesion_indices_for_one_text(text=text), ignore_index=True)
        end = time.time()  
        print(f'Tiempo demorado: {end - start} segundos.')
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