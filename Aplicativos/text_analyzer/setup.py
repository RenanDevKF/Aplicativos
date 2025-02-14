from setuptools import setup, find_packages

# Configuração do pacote para distribuição
setup(
    name="text_analyzer",  # Nome do pacote
    version="0.1.0",  # Versão do pacote
    packages=find_packages(),  # Descobre automaticamente os subpacotes

    # Dependências do projeto
    install_requires=[
        'pandas',  # Manipulação de dados
        'matplotlib',  # Visualização de gráficos
        'wordcloud',  # Geração de nuvens de palavras
        'nltk',  # Processamento de linguagem natural
    ],

    # Informações do autor
    author="Renan Kirchmaier Fayer",
    author_email="renan.devkf@gmail.com",

    # Descrição do pacote
    description="Um analisador de vocabulário de texto em Python",
    long_description=open('README.md').read(),  # Descrição longa retirada do README
    long_description_content_type="text/markdown",  # Define o formato do README
)
