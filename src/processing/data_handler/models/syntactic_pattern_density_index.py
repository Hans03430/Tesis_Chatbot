from src.processing.data_handler import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class SyntacticPatternDensityIndex(Base):
    '''
    This is the class that represents the syntactic pattern density indices of a text.
    '''
    __tablename__ = 'SYNTACTIC_PATTERN_DENSITY_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='syntactic_pattern_density_index')
    DRNP = Column('DRNP', Float, nullable=True)
    DRVP = Column('DRVP', Float, nullable=True)
    DRNEG = Column('DRNEG', Float, nullable=True)


