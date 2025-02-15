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
        TypeError: Se `file_path` não for um `str` ou `TextIO`.
        FileNotFoundError: Se o caminho do arquivo não existir.
        IOError: Se houver erro ao abrir ou ler o arquivo.
        ValueError: Se o arquivo estiver vazio.

    Exemplo:
        > content = read_file("exemplo.txt")
        > print(content)  # Exibe o conteúdo do arquivo

    Nota:
        Se um arquivo vazio for passado, a função levantará um `ValueError`.
        Se um erro inesperado ocorrer durante a leitura do arquivo, será levantado um `IOError`.
    """
    if not isinstance(file_path, (str, TextIO)):
        raise TypeError("Erro: O parâmetro 'file_path' deve ser um caminho de arquivo (str) ou um objeto file-like (TextIO).")

    try:
        if isinstance(file_path, str):
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Erro: O arquivo '{file_path}' não foi encontrado.")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = file_path.read()
        
        if not content.strip():
            raise ValueError(f"Erro: O arquivo '{file_path}' está vazio.")

        return content

    except IOError as e:
        raise IOError(f"Erro ao abrir ou ler o arquivo: {str(e)}")
