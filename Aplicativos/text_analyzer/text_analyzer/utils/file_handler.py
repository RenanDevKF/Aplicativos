from typing import Union, TextIO
import os
import pdfplumber

def read_file(file_path: Union[str, TextIO]) -> str:
    """
    Lê um arquivo de texto ou PDF e retorna seu conteúdo como uma string.

    A função aceita tanto um caminho de arquivo (`str`) quanto um objeto file-like (`TextIO`).
    Se for passado um caminho de arquivo `.txt`, o arquivo será aberto e lido com codificação UTF-8.
    Se for passado um arquivo `.pdf`, o texto será extraído utilizando a biblioteca `pdfplumber`.

    Args:
        file_path (Union[str, TextIO]): Caminho do arquivo ou objeto file-like.

    Returns:
        str: Conteúdo do arquivo como string.

    Raises:
        TypeError: Se `file_path` não for um `str` ou `TextIO`.
        FileNotFoundError: Se o caminho do arquivo não existir.
        IOError: Se houver erro ao abrir ou ler o arquivo.
        ValueError: Se o arquivo estiver vazio ou no formato não suportado.
        ValueError: Se o conteúdo do PDF não puder ser extraído.

    Exemplo:
        > content = read_file("exemplo.txt")
        > print(content)  # Exibe o conteúdo do arquivo

    Nota:
        Se um arquivo vazio for passado, a função levantará um `ValueError`.
        Se um erro inesperado ocorrer durante a leitura do arquivo, será levantado um `IOError`.
        Se o arquivo for PDF e não puder ser extraído, um erro será levantado.
    """
    if not isinstance(file_path, (str, TextIO)):
        raise TypeError("Erro: O parâmetro 'file_path' deve ser um caminho de arquivo (str) ou um objeto file-like (TextIO).")

    try:
        if isinstance(file_path, str):
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Erro: O arquivo '{file_path}' não foi encontrado.")
            
            # Se o arquivo for .txt
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

            # Se o arquivo for .pdf
            elif ext.lower() == ".pdf":
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                content = text.strip() if text else "Nenhum texto encontrado no PDF."
                
                if not content.strip():
                    raise ValueError(f"Erro: Não foi possível extrair texto do PDF '{file_path}'.")

            else:
                raise ValueError(f"Erro: O formato do arquivo '{ext}' não é suportado.")
        
        else:
            content = file_path.read()

        if not content.strip():
            raise ValueError(f"Erro: O arquivo '{file_path}' está vazio.")

        return content

    except IOError as e:
        raise IOError(f"Erro ao abrir ou ler o arquivo: {str(e)}")

    except ValueError as e:
        raise ValueError(str(e))
