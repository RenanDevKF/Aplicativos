import re
from typing import List

def clean_text(text: str) -> List[str]:
    """
    Limpa e normaliza o texto
    - Remove pontuação
    - Converte para minúsculas
    - Remove stopwords
    """
    # Converte para minúsculas
    text = text.lower()
    
    # Remove pontuação
    text = re.sub(r'[^\w\s]', '', text)
    
    # Divide em palavras
    words = text.split()
    
    return words