from typing import Union, TextIO
import os

def read_file(file_path: Union[str, TextIO]) -> str:
    """
    Lê um arquivo de texto e retorna seu conteúdo
    Suporta tanto caminhos de arquivo quanto objetos file-like
    """
    if isinstance(file_path, str):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return file_path.read()