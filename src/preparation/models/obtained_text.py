from src.preparation import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.preparation.models.descriptive_index import DescriptiveIndex
from src.preparation.models.connective_index import ConnectiveIndex
from src.preparation.models.lexical_diversity_index import LexicalDiversityIndex
from src.preparation.models.readability_index import ReadabilityIndex
from src.preparation.models.referential_cohesion_index import ReferentialCohesionIndex
from src.preparation.models.syntactic_complexity_index import SyntacticComplexityIndex
from src.preparation.models.syntactic_pattern_density_index import SyntacticPatternDensityIndex
from src.preparation.models.word_information_index import WordInformationIndex
from typing import Dict


class ObtainedText(Base):
    '''
    This is the class that represents a downloaded text with all its attributes like those calculated by the text analyzer tool.
    '''
    __tablename__ = 'OBTAINED_TEXT'

    id = Column('ID', Integer, primary_key=True)
    text = Column('TEXT', String, nullable=False)
    filename = Column('FILENAME', String(256), nullable=False)
    grade = Column('GRADE', Integer, nullable=False)
    category = Column('CATEGORY', String, nullable=False)
    cluster_grade = Column('CLUSTER_GRADE', Integer, nullable=True)
    descriptive_index = relationship('DescriptiveIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    connective_index = relationship('ConnectiveIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    lexical_diversity_index = relationship('LexicalDiversityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    readability_index = relationship('ReadabilityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete-orphan, merge')
    referential_cohesion_index = relationship('ReferentialCohesionIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    syntactic_complexity_index = relationship('SyntacticComplexityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    syntactic_pattern_density_index = relationship('SyntacticPatternDensityIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')
    word_information_index = relationship('WordInformationIndex', uselist=False, lazy='joined', back_populates='obtained_text', cascade='save-update, delete, delete-orphan, merge')

    def to_dict(self) -> Dict:
        '''
        This method transforms this object into a python dictionary.

        Parameters:
        None.

        Returns:
        Dict: The dictionary representation of the data of this object.
        '''
        return {
            'id': self.id,
            'text': self.text,
            'filename': self.filename,
            'grade': self.grade,
            'category': self.category,
            'cluster_grade': self.cluster_grade,
            'descriptive_index': None if self.descriptive_index is None else self.descriptive_index.to_dict(),
            'connective_index': None if self.connective_index is None else self.connective_index.to_dict(),
            'lexical_diversity_index': None if self.lexical_diversity_index is None else self.lexical_diversity_index.to_dict(),
            'readability_index': None if self.readability_index is None else self.readability_index.to_dict(),
            'referential_cohesion_index': None if self.referential_cohesion_index is None else self.referential_cohesion_index.to_dict(),
            'syntactic_complexity_index': None if self.syntactic_complexity_index is None else self.syntactic_complexity_index.to_dict(),
            'syntactic_pattern_density_index': None if self.syntactic_pattern_density_index is None else self.syntactic_pattern_density_index.to_dict(),
            'word_information_index': None if self.word_information_index is None else self.word_information_index.to_dict(),
        }