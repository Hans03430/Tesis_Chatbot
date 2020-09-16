import spacy

from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger

if __name__ == "__main__":
    nlp = spacy.load('es_core_news_lg', disable=['ner'])
    nlp.add_pipe(VerbPhraseTagger(nlp, 'es'), after='parser')
    text = '''Carro.

Yo tengo hermosos buenos Carros.

Carros.
'''
    doc = nlp(text)
    for token in doc:
        if token.is_alpha:
            print(token, token.pos_, token.tag_)