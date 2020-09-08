import spacy

from src.processing.pipes.verb_phrase_tagger import VerbPhraseTagger

if __name__ == "__main__":
    nlp = spacy.load('es_core_news_sm', disable=['ner'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    nlp.add_pipe(VerbPhraseTagger(nlp, 'es'), after='parser')
    text = '''El profesor dio por acabada la lección.
'''
    doc = nlp(text)
    print(nlp.pipe_names)