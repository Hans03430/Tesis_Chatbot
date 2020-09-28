import pandas as pd

from src.preparation import session
from src.preparation.models.obtained_text import ObtainedText
from typing import List

class ObtainedTextDA:
    '''
    This class will handle all CRUD operations on the instances of ObtainedText class.
    '''
    def __init__(self):
        pass

    def insert(self, ot: ObtainedText) -> None:
        '''
        This method handles insertion of instances of ObtainedText to the database.

        Parameters:
        ot(ObtainedText): The object that will be inserted.

        Returns:
        None.
        '''
        try:
            if ot.id is None:
                session.add(ot)
                session.commit()
        except Exception as e:
            session.rollback()
            raise(e)

    def update(self, ot: ObtainedText) -> None:
        '''
        This method updates a single ObtainedText instance.

        Parameters:
        ot(ObtainedText): The ObtainedText instance with new data to update.

        Returns:
        None.
        '''
        try:
            if ot.id is not None:
                session.commit()
            else:
                raise AttributeError('The Text doesn\'t exist in the database.')
        except Exception as e:
            session.rollback()
            raise(e)

    def select_all(self) -> List[ObtainedText]:
        '''
        This method returns all obtained text instances and their indices.

        Parameters:
        None.

        Returns:
        List[ObtainedText]: The list of all instances of ObtainedTexts.
        '''
        try:
            return session.query(ObtainedText).all()
        except Exception as e:
            raise e

    def select_all_as_dataframe(self) -> pd.DataFrame:
        '''
        This method returns all obtained text instances and their indices as a pandas Dataframe. It excludes the 'text' field.

        Parameters:
        None.

        Returns:
        pd.DataFrame: The dataframe of all instances of ObtainedTexts.
        '''
        try:
            texts = self.select_all()
            dataframe = pd.DataFrame()

            for t in texts:
                row = {}
                text_as_dict = t.to_dict()
                
                for key in ['id', 'grade', 'category', 'filename', 'cluster_grade']: # Add text's basic information
                    row[key] = text_as_dict[key]
                # Add the information of all indices
                for index_key in ['descriptive_index', 'connective_index', 'lexical_diversity_index', 'readability_index', 'referential_cohesion_index', 'syntactic_complexity_index', 'syntactic_pattern_density_index', 'word_information_index']:
                    index = text_as_dict[index_key]
                    if index is not None:
                        for key in index:
                            if key not in ['id', 'obtained_text_id', 'obtained_text']:
                                row[key] = index[key]
                
                dataframe = dataframe.append(row, ignore_index=True)
            return dataframe
        except Exception as e:
            raise e

