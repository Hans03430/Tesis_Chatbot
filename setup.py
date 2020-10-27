from setuptools import find_packages, setup

setup(
    name='tesis_chatbot',
    author='Hans Matos Rios',
    author_email='hans.matos@pucp.edu.pe',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'aiohttp',
        'aiofile',
        'beautifulsoup4',
        'spacy',
        'tika',
        'Pyphen',
        'pandas',
        'SQLAlchemy',
        'scikit-learn',
        'scikit-plot',
        'seaborn',
        'text-complexity-analyzer-cm @ https://github.com/Hans03430/TextComplexityAnalyzerCM/tarball/master#egg=text-complexity-analyzer-cm-0.1.0'
    ]
)

