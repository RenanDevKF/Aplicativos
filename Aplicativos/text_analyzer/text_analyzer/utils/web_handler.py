import requests
from bs4 import BeautifulSoup

def fetch_webpage_text(url: str) -> str:
    """
    Faz o download do conteúdo de uma página da web e extrai o texto limpo.

    A função acessa uma URL fornecida, realiza o download da página e extrai o texto relevante dos elementos HTML (p, div, span).
    Se a página for acessada com sucesso, retorna o texto extraído. Se houver erro ao acessar a página ou ao processar o conteúdo,
    serão levantadas exceções específicas.

    Args:
        url (str): URL da página a ser analisada.

    Returns:
        str: Texto extraído da página, limpo e sem tags HTML.

    Raises:
        requests.RequestException: Se houver erro ao acessar a página (ex: falha de conexão, timeout, etc.).
        ValueError: Se a URL não for válida ou se não for possível extrair texto relevante da página.

    Exemplo:
        > url = "https://www.exemplo.com"
        > text = fetch_webpage_text(url)
        > print(text)  # Exibe o texto extraído da página

    Nota:
        Caso o conteúdo extraído não tenha texto relevante, a função retorna uma mensagem padrão: "Nenhum texto relevante encontrado na página."
    """
    if not isinstance(url, str) or not url.startswith('http'):
        raise ValueError(f"Erro: A URL fornecida '{url}' não é válida ou não começa com 'http'.")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Levanta um erro se o status HTTP for um código de erro (404, 500, etc.)

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all(["p", "div", "span"])  # Busca por parágrafos, divs e spans

        # Extrai e limpa o texto dos elementos encontrados
        text = "\n".join([p.get_text(strip=True) for p in paragraphs])

        if not text.strip():
            raise ValueError(f"Erro: Nenhum texto relevante encontrado na página '{url}'.")

        return text.strip()

    except requests.RequestException as e:
        raise requests.RequestException(f"Erro ao acessar a página '{url}': {e}")

    except ValueError as e:
        raise ValueError(f"Erro ao processar o conteúdo da página '{url}': {e}")

    except Exception as e:
        raise Exception(f"Erro inesperado ao acessar ou processar a página '{url}': {e}")

