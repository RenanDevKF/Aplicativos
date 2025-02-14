from setuptools import setup, find_packages

setup(
    name="text_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'wordcloud',
        'nltk',
    ],
    author="Renan Kirchmaier Fayer",
    author_email="renan.devkf@gmail.com",
    description="Um analisador de vocabulário de texto em Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)