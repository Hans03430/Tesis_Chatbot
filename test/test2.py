import spacy

from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger

if __name__ == "__main__":
    nlp = spacy.load('es_core_news_sm', disable=['ner'])
    nlp.add_pipe(VerbPhraseTagger(nlp, 'es'), after='parser')
    text = '''Yo hago mis tareas todos los días.
Nosotros conocemos unos buenos alumnos.

Él y su familia irán de paseo mañana.
Por otro lado, ella sacará a pasear a su hermoso perro negro.

Ellos jugarán baloncesto con ellas toda la semana.
Tu me debes mucho dinero y ustedes no lo saben.
'''
    doc = nlp(text)
    for token in doc:
        if token.is_alpha:
            print(token, token.pos_, token.tag_)