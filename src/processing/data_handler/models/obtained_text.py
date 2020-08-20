from src.processing.data_handler import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.processing.data_handler.models.descriptive_index import DescriptiveIndex
from src.processing.data_handler.models.connective_index import ConnectiveIndex
from src.processing.data_handler.models.lexical_diversity_index import LexicalDiversityIndex
from src.processing.data_handler.models.readability_index import ReadabilityIndex
from src.processing.data_handler.models.referential_cohesion_index import ReferentialCohesionIndex
from src.processing.data_handler.models.syntactic_complexity_index import SyntacticComplexityIndex
from src.processing.data_handler.models.syntactic_pattern_density_index import SyntacticPatternDensityIndex
from src.processing.data_handler.models.word_information_index import WordInformationIndex


class ObtainedText(Base):
    '''
    This is the class that represents a downloaded text with all its attributes like those calculated by the text analyzer tool.
    '''
    __tablename__ = 'OBTAINED_TEXT'

    id = Column('ID', Integer, primary_key=True)
    text = Column('TEXT', String, nullable=False)
    filename = Column('FILENAME', String(256), nullable=False)
    grade = Column('GRADE', Integer, nullable=False)
    descriptive_index = relationship('DescriptiveIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    connective_index = relationship('ConnectiveIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    lexical_diversity_index = relationship('LexicalDiversityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    readability_index = relationship('ReadabilityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete-orphan, merge')
    referential_cohesion_index = relationship('ReferentialCohesionIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    syntactic_complexity_index = relationship('SyntacticComplexityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    syntactic_pattern_density_index = relationship('SyntacticPatternDensityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    word_information_index = relationship('WordInformationIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
