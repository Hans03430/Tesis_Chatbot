from src.preparation import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict


class SentencePair(Base):
    '''
    This is the class that represents a pair of sentences from the text.
    '''
    __tablename__ = 'SENTENCE PAIR'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='sentence_pair')
    first = Column('FIRST', String, nullable=False)
    second = Column('SECOND', String, nullable=False)

    def to_dict(self) -> Dict:
        '''
        This method transforms this object into a python dictionary.

        Parameters:
        None.

        Returns:
        Dict: The dictionary representation of the data of this object.
        '''
        values = self.__dict__
        values.pop('_sa_instance_state', None)
        return values
