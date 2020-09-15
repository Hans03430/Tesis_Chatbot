from src.preparation import Base
from src.preparation import engine
from src.preparation.models.obtained_text import ObtainedText
from src.preparation.models.descriptive_index import DescriptiveIndex

from src.preparation.models.descriptive_index import DescriptiveIndex
from src.preparation.models.connective_index import ConnectiveIndex
from src.preparation.models.lexical_diversity_index import LexicalDiversityIndex
from src.preparation.models.readability_index import ReadabilityIndex
from src.preparation.models.referential_cohesion_index import ReferentialCohesionIndex
from src.preparation.models.syntactic_complexity_index import SyntacticComplexityIndex
from src.preparation.models.syntactic_pattern_density_index import SyntacticPatternDensityIndex
from src.preparation.models.word_information_index import WordInformationIndex


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)