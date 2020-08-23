from src.processing.data_handler import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict


class DescriptiveIndex(Base):
    '''
    This is the class that represents the descriptive indices of a text.
    '''
    __tablename__ = 'DESCRIPTIVE_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='descriptive_index')
    DESPC = Column('DESPC', Float, nullable=True)
    DESSC = Column('DESSC', Float, nullable=True)
    DESWC = Column('DESWC', Float, nullable=True)
    DESPL = Column('DESPL', Float, nullable=True)
    DESPLd = Column('DESPLd', Float, nullable=True)
    DESSL = Column('DESSL', Float, nullable=True)
    DESSLd = Column('DESSLd', Float, nullable=True)
    DESWLsy = Column('DESWLsy', Float, nullable=True)
    DESWLsyd = Column('DESWLsyd', Float, nullable=True)
    DESWLlt = Column('DESWLlt', Float, nullable=True)
    DESWLltd = Column('DESWLltd', Float, nullable=True)

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