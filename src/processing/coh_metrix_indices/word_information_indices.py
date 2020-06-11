import spacy

from src.processing.constants import ACCEPTED_LANGUAGES

def get_word_grammatical_information(text: str, language: str='es'):
    '''
    This function calculates the grammatical incident of the words.

    Parameters:
    text(str): The text to be split into sentences.
    language(str): The language of the text.

    Returns:
    None
    '''
    if len(text) == 0:
        raise ValueError('The word is empty.')
    elif not language in ACCEPTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet')

    nlp = spacy.load('es', disable=['parser', 'ner'])
    text_spacy = nlp(text)

    nouns = [token
             for token in text_spacy
             if not token.is_punct and token.pos_ == 'NOUN'] # Find the nouns in the text

    verbs = [token
             for token in text_spacy
             if not token.is_punct and token.pos_ == 'VERB'] # Find the verbs in the text

    adjectives = [token
                  for token in text_spacy
                  if not token.is_punct and token.pos_ == 'ADJ'] # Find the adjectives in the text

    adverbs = [token
               for token in text_spacy
               if not token.is_punct and token.pos_ == 'ADV'] # Find the adverbs in the text

    pronouns = [token
                for token in text_spacy
                if not token.is_punct and token.pos_ == 'PRON'] # Find the personal pronouns
    
    personal_pronouns = [token
                         for token in pronouns
                         if 'PronType=Prs' in token.tag_]

    personal_pronouns_first_person_single_form = [token
                                                  for token in personal_pronouns
                                                  if 'Number=Sing' in token.tag_ and 'Person=1' in token.tag_]
    
    personal_pronouns_first_person_plural_form = [token
                                                  for token in personal_pronouns
                                                  if 'Number=Plur' in token.tag_ and 'Person=1' in token.tag_]
    
    personal_pronouns_second_person_single_form = [token
                                                  for token in personal_pronouns
                                                  if 'Number=Sing' in token.tag_ and 'Person=2' in token.tag_]
    
    personal_pronouns_second_person_plural_form = [token
                                                  for token in personal_pronouns
                                                  if 'Number=Plur' in token.tag_ and 'Person=2' in token.tag_]
    
    personal_pronouns_third_person_single_form = [token
                                                  for token in personal_pronouns
                                                  if 'Number=Sing' in token.tag_ and 'Person=3' in token.tag_]
    
    personal_pronouns_third_person_plural_form = [token
                                                  for token in personal_pronouns
                                                  if 'Number=Plur' in token.tag_ and 'Person=3' in token.tag_]
    
    return len(nouns), len(verbs), len(adjectives), len(adverbs), len(personal_pronouns), len(personal_pronouns_first_person_single_form), len(personal_pronouns_first_person_plural_form), len(personal_pronouns_second_person_single_form), len(personal_pronouns_second_person_plural_form), len(personal_pronouns_third_person_single_form), len(personal_pronouns_third_person_plural_form)