import pytest
from text_analyzer.utils.web_handler import fetch_webpage_text
from unittest.mock import Mock
import requests

def test_fetch_webpage_text_success(mocker):
    """Testa se a função retorna corretamente o texto extraído quando a resposta HTTP é válida."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><h1>Vaga Exemplo</h1><p>Descrição da vaga</p></body></html>"
    mocker.patch("requests.get", return_value=mock_response)

    # Simula um seletor existente no SELECTORS para teste
    mocker.patch("job_matcher.config.selectors.SELECTORS", {"exemplo.com": {"title": "h1"}})

    result = fetch_webpage_text("http://exemplo.com")

    assert "title" in result
    assert result["title"] == "Vaga Exemplo"

def test_fetch_webpage_text_empty_response(mocker):
    """Testa se a função retorna valores padrão quando a resposta está vazia."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = ""
    mocker.patch("requests.get", return_value=mock_response)

    mocker.patch("job_matcher.config.selectors.SELECTORS", {"exemplo.com": {"title": "h1"}})

    result = fetch_webpage_text("http://exemplo.com")
    assert result["title"] == "N/A"

def test_fetch_webpage_text_error_status(mocker):
    """Testa se a função retorna um erro quando recebe um código HTTP inválido."""
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.text = "Página não encontrada"
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_webpage_text("http://exemplo.com")
    
    assert "erro" in result
    assert "404" in result["erro"]

def test_fetch_webpage_text_invalid_html(mocker):
    """Testa se a função ainda extrai texto mesmo quando o HTML está malformado."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><h1>Vaga Exemplo"
    mocker.patch("requests.get", return_value=mock_response)

    mocker.patch("job_matcher.config.selectors.SELECTORS", {"exemplo.com": {"title": "h1"}})

    result = fetch_webpage_text("http://exemplo.com")
    assert result["title"] == "Vaga Exemplo"

def test_fetch_webpage_text_request_timeout(mocker):
    """Testa se a função retorna um erro quando ocorre timeout na requisição."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    result = fetch_webpage_text("http://exemplo.com")

    assert "erro" in result
    assert "Timeout" in result["erro"]

def test_fetch_webpage_text_invalid_url():
    """Testa se a função retorna erro ao receber uma URL inválida."""
    result = fetch_webpage_text("")
    assert "erro" in result
    assert "URL" in result["erro"]
