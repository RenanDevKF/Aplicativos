import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from text_analyzer.job_matcher.config.selectors import SELECTORS



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

def salvar_em_json(dados, caminho_arquivo):
    """
    Salva os dados extraídos em um arquivo JSON.

    Args:
        dados (dict): Dados a serem salvos.
        caminho_arquivo (str): Caminho completo do arquivo JSON.
    """
    try:
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

        # Salva os dados no formato JSON
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos em: {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

# Função para ler os links do arquivo
def ler_links_do_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        links = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    return links

# Caminho para o arquivo com os links
caminho_arquivo = os.path.join(os.path.dirname(__file__), '..', 'job_matcher', 'config', 'links_vagas.txt')

# Ler os links do arquivo
urls = ler_links_do_arquivo(caminho_arquivo)

# Dicionário para armazenar os textos extraídos de cada página
vaga_textos = {}

# Extrair os textos de cada URL
for url in urls:
    vaga_textos[url] = fetch_webpage_text(url)

# Pega o diretório raiz do projeto (text_analyzer/text_analyzer)
diretorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
caminho_json = os.path.join(diretorio_base, 'job_matcher', 'config', 'vagas_extraidas.json')

# Salvar os dados extraídos no arquivo JSON
salvar_em_json(vaga_textos, caminho_json)
