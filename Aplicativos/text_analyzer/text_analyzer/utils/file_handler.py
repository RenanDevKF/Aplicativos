from typing import Union, TextIO
import os

def read_file(file_path: Union[str, TextIO]) -> str:
    """
    Lê um arquivo de texto e retorna seu conteúdo como uma string.

    A função aceita tanto um caminho de arquivo (`str`) quanto um objeto file-like (`TextIO`).
    Se for passado um caminho de arquivo, o arquivo será aberto e lido com codificação UTF-8.

    Args:
        file_path (Union[str, TextIO]): Caminho do arquivo ou objeto file-like.

    Returns:
        str: Conteúdo do arquivo como string.

    Raises:
        FileNotFoundError: Se o caminho do arquivo não existir.
        IOError: Se houver erro ao abrir ou ler o arquivo.

    Exemplo:
        > content = read_file("exemplo.txt")
        > print(content)  # Exibe o conteúdo do arquivo
    """
    if isinstance(file_path, str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado.")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return file_path.read()
