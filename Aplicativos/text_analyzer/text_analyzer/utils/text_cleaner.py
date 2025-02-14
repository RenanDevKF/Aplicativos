import re
from typing import List

def clean_text(text: str) -> List[str]:
    """
    Processa e normaliza um texto, removendo pontuação e convertendo para minúsculas.

    Args:
        text (str): O texto de entrada a ser processado.

    Returns:
        List[str]: Lista de palavras limpas extraídas do texto.
    
    Exemplo:
        > clean_text("Olá, mundo! Isso é um teste.")
        ['olá', 'mundo', 'isso', 'é', 'um', 'teste']
    """
    # Converte para minúsculas
    text = text.lower()
    
    # Remove pontuação
    text = re.sub(r'[^\w\s]', '', text)
    
    # Divide em palavras
    words = text.split()
    
    return words
