from src.processing.data_handler import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class SyntacticComplexityIndex(Base):
    '''
    This is the class that represents the syntactic complexity indices of a text.
    '''
    __tablename__ = 'SYNTACTIC_COMPLEXITY_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='syntactic_complexity_index')
    SYNNP = Column('SYNNP', Float, nullable=True)
    SYNLE = Column('SYNLE', Float, nullable=True)


