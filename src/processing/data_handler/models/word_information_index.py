from src.processing.data_handler import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict


class WordInformationIndex(Base):
    '''
    This is the class that represents the syntactic pattern density indices of a text.
    '''
    __tablename__ = 'WORD_INFORMATION_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='word_information_index')
    WRDNOUN = Column('WRDNOUN', Float, nullable=True)
    WRDVERB = Column('WRDVERB', Float, nullable=True)
    WRDADJ = Column('WRDADJ', Float, nullable=True)
    WRDADV = Column('WRDADV', Float, nullable=True)
    WRDPRO = Column('WRDPRO', Float, nullable=True)
    WRDPRP1s = Column('WRDPRP1s', Float, nullable=True)
    WRDPRP1p = Column('WRDPRP1p', Float, nullable=True)
    WRDPRP2s = Column('WRDPRP2s', Float, nullable=True)
    WRDPRP2p = Column('WRDPRP2p', Float, nullable=True)
    WRDPRP3s = Column('WRDPRP3s', Float, nullable=True)
    WRDPRP3p = Column('WRDPRP3p', Float, nullable=True)
        
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
