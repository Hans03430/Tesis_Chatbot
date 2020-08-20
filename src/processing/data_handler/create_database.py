from src.processing.data_handler import Base
from src.processing.data_handler import engine
from src.processing.data_handler.models.obtained_text import ObtainedText
from src.processing.data_handler.models.descriptive_index import DescriptiveIndex

from src.processing.data_handler.models.descriptive_index import DescriptiveIndex
from src.processing.data_handler.models.connective_index import ConnectiveIndex
from src.processing.data_handler.models.lexical_diversity_index import LexicalDiversityIndex
from src.processing.data_handler.models.readability_index import ReadabilityIndex
from src.processing.data_handler.models.referential_cohesion_index import ReferentialCohesionIndex
from src.processing.data_handler.models.syntactic_complexity_index import SyntacticComplexityIndex
from src.processing.data_handler.models.syntactic_pattern_density_index import SyntacticPatternDensityIndex
from src.processing.data_handler.models.word_information_index import WordInformationIndex


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)