from src.processing.data_handler import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class ConnectiveIndex(Base):
    '''
    This is the class that represents the connective indices of a text.
    '''
    __tablename__ = 'CONNECTIVE_INDEX'

    id = Column('ID', Integer, primary_key=True)
    obtained_text_id = Column('OBTAINED_TEXT_ID', ForeignKey('OBTAINED_TEXT.ID'))
    obtained_text = relationship('ObtainedText', back_populates='connective_index')
    CNCAll = Column('CNCAll', Float, nullable=True)
    CNCCaus = Column('CNCCaus', Float, nullable=True)
    CNCLogic = Column('CNCLogic', Float, nullable=True)
    CNCADC = Column('CNCADC', Float, nullable=True)
    CNCTemp = Column('CNCTemp', Float, nullable=True)
    CNCAdd = Column('CNCAdd', Float, nullable=True)
