from src.processing.data_handler import session
from src.processing.data_handler.models.obtained_text import ObtainedText
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
