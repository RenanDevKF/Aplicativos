import re
from typing import List
from nltk.corpus import stopwords
import nltk

# Baixa as stopwords caso necessário
try:
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words("portuguese"))
except Exception as e:
    STOP_WORDS = set()
    print(f"Aviso: Não foi possível carregar as stopwords. Erro: {e}")

def clean_text(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Processa e normaliza um texto, removendo pontuação e convertendo para minúsculas.
    Também pode remover stopwords se o parâmetro remove_stopwords for True.

    Args:
        text (str): O texto de entrada a ser processado.
        remove_stopwords (bool): Se True, remove stopwords do texto.

    Returns:
        List[str]: Lista de palavras limpas extraídas do texto.

    Raises:
        TypeError: Se `text` não for uma string.
        ValueError: Se `text` estiver vazio.

    Exemplo:
        > clean_text("Olá, mundo! Python é incrível.")
        ['ola', 'mundo', 'python', 'e', 'incrivel']
    """
    if not isinstance(text, str):
        raise TypeError("O parâmetro 'text' deve ser uma string.")
    
    if not text.strip():
        raise ValueError("O texto fornecido está vazio.")

    text = text.lower()  # Converte para minúsculas
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    words = text.split()  # Divide o texto em palavras
    
    if remove_stopwords and STOP_WORDS:
        words = [word for word in words if word not in STOP_WORDS]

    return words