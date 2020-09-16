import spacy

from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger

if __name__ == "__main__":
    nlp = spacy.load('es_core_news_lg', disable=['ner'])
    nlp.add_pipe(VerbPhraseTagger(nlp, 'es'), after='parser')
    text = '''Ellos jugaron todo el día. Ellas no participaron en el juego.

Yo juego con el hermoso gato. A nosotros no nos gusta el gato.

Ella tiene mascotas. Ella tiene plantas y él no.

Tú jamás dijiste que no.
Ustedes salieron temprano en la hermosa mañana.
'''
    doc = nlp(text)
    for token in doc:
        if token.is_alpha:
            print(token, token.lemma_, token.pos_, token.tag_)