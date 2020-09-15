from src.preparation import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict


class ReferentialCohesionIndex(Base):
    '''
    This is the class that represents the referential cohesion indices of a text.
    '''
    __tablename__ = 'REFERENTIAL_COHESION_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='referential_cohesion_index')
    CRFNO1 = Column('CRFNO1', Float, nullable=True)
    CRFNOa = Column('CRFNOa', Float, nullable=True)
    CRFAO1 = Column('CRFAO1', Float, nullable=True)
    CRFAOa = Column('CRFAOa', Float, nullable=True)
    CRFSO1 = Column('CRFSO1', Float, nullable=True)
    CRFSOa = Column('CRFSOa', Float, nullable=True)
    CRFCWO1 = Column('CRFCWO1', Float, nullable=True)
    CRFCWO1d = Column('CRFCWO1d', Float, nullable=True)
    CRFCWOa = Column('CRFCWOa', Float, nullable=True)
    CRFCWOad = Column('CRFCWOad', Float, nullable=True)
    CRFANP1 = Column('CRFANP1', Float, nullable=True)
    CRFANPa = Column('CRFANPa', Float, nullable=True)

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