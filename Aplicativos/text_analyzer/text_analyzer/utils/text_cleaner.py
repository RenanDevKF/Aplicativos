import re
from typing import List
from nltk.corpus import stopwords
import nltk

# Baixa as stopwords caso necessário
nltk.download('stopwords')

def clean_text(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Processa e normaliza um texto, removendo pontuação e convertendo para minúsculas.
    Também pode remover stopwords se o parâmetro remove_stopwords for True.

    Args:
        text (str): O texto de entrada a ser processado.
        remove_stopwords (bool): Se True, remove stopwords do texto.

    Returns:
        List[str]: Lista de palavras limpas extraídas do texto.
    """
    text = text.lower()  # Converte para minúsculas
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    words = text.split()  # Divide o texto em palavras
    
    if remove_stopwords:
        stop_words = set(stopwords.words("portuguese"))
        words = [word for word in words if word not in stop_words]

    return words

