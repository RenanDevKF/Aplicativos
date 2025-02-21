from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from job_matcher.config.selectors import SELECTORS

def fetch_webpage_text(url: str) -> dict:
    """
    Busca e extrai informações estruturadas de uma página de vaga de emprego.
    
    Args:
        url (str): URL da vaga de emprego.

    Returns:
        dict: Dicionário contendo título, descrição, empresa e localização da vaga,
              ou uma chave "erro" em caso de falha.
    """
    try:
        if not isinstance(url, str) or not url.strip():
            raise ValueError("A URL fornecida é inválida ou está vazia.")

        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Levanta erro para códigos HTTP de falha
    
        soup = BeautifulSoup(response.text, "html.parser")

        # Detecta o site baseado no domínio
        domain = urlparse(url).netloc.replace("www.", "")
        if domain not in SELECTORS:
            raise KeyError(f"Seletores não configurados para o domínio: {domain}")

        # Extrai as informações da vaga
        selectors = SELECTORS[domain]
        vaga_info = {}
        
        for key in ["title", "description", "company", "location"]:
            try:
                vaga_info[key] = (
                    soup.select_one(selectors[key]).get_text(strip=True)
                    if selectors.get(key) and soup.select_one(selectors[key])
                    else "N/A"
                )
            except Exception as e:
                vaga_info[key] = "Erro ao extrair"
                vaga_info[f"erro_{key}"] = str(e)
                
        return vaga_info

    except requests.exceptions.RequestException as req_err:
        return {"erro": f"Erro na requisição HTTP: {str(req_err)}"}
    except KeyError as key_err:
        return {"erro": f"Erro de configuração: {str(key_err)}"}
    except ValueError as val_err:
        return {"erro": f"Erro de validação: {str(val_err)}"}
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}
