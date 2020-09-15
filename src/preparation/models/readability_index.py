from src.preparation import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict


class ReadabilityIndex(Base):
    '''
    This is the class that represents the readability indices of a text.
    '''
    __tablename__ = 'READABILITY_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='readability_index')
    RDFHGL = Column('RDFHGL', Float, nullable=True)

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