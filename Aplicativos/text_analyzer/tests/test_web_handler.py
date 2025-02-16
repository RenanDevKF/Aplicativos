import pytest
from text_analyzer.utils.web_handler import fetch_webpage_text
from unittest.mock import Mock
import requests

def test_fetch_webpage_text_success(mocker):
    # Simulando uma resposta HTTP bem-sucedida com conteúdo HTML simples
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><p>Texto extraído</p></body></html>"
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_webpage_text("http://exemplo.com")
    assert "Texto extraído" in result
    assert result == "Texto extraído"  # Verifica que o texto correto é extraído

def test_fetch_webpage_text_empty_response(mocker):
    # Simulando uma resposta vazia
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = ""
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_webpage_text("http://exemplo.com")
    assert result == "Nenhum texto relevante encontrado na página."  # Espera a mensagem padrão

def test_fetch_webpage_text_error_status(mocker):
    # Simulando uma resposta com erro HTTP (404)
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.text = "Página não encontrada"
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_webpage_text("http://exemplo.com")
    
    # Verificando se a resposta contém a descrição do erro de status
    assert "404" in result  # Verifica se o código de status 404 está na resposta
    assert "Página não encontrada" in result  # Verifica se a descrição do erro está na resposta

    

def test_fetch_webpage_text_invalid_html(mocker):
    # Simulando uma resposta com HTML malformado
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><p>Texto extraído"
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_webpage_text("http://exemplo.com")
    assert "Texto extraído" in result  # Espera o texto ser extraído, mesmo com HTML malformado

def test_fetch_webpage_text_request_timeout(mocker):
    # Simulando um erro de timeout ao fazer a requisição
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(requests.exceptions.Timeout):
        fetch_webpage_text("http://exemplo.com")
