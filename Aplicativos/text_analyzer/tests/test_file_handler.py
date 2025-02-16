import pytest
import os
from io import StringIO
from unittest.mock import patch
from text_analyzer.utils.file_handler import read_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Fixture para criar e remover um arquivo PDF temporário realista
@pytest.fixture
def temp_pdf_file():
    file_path = "temp_vaga_python.pdf"
    # Usando reportlab para criar um PDF com conteúdo realista
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "Vaga para Desenvolvedor Python - Remoto")
    c.drawString(100, 730, "Procuramos um desenvolvedor Python com experiência em frameworks como Django ou Flask.")
    c.drawString(100, 710, "A experiência com análise de dados e bibliotecas como Pandas e NumPy será um diferencial.")
    c.drawString(100, 690, "Requisitos:")
    c.drawString(100, 670, "- Python 3.x")
    c.drawString(100, 650, "- Experiência com Git")
    c.drawString(100, 630, "- Familiaridade com APIs RESTful")
    c.save()  # Salva o arquivo PDF
    yield file_path
    os.remove(file_path)

# Fixture para criar e remover um arquivo TXT temporário
@pytest.fixture
def temp_txt_file():
    file_path = "temp_vaga_python.txt"
    texto_txt = """
    Vaga para Desenvolvedor Python - Remoto
    Procuramos um desenvolvedor Python com experiência em frameworks como Django ou Flask.
    A experiência com análise de dados e bibliotecas como Pandas e NumPy será um diferencial.
    Requisitos:
        - Python 3.x
        - Experiência com Git
        - Familiaridade com APIs RESTful
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(texto_txt)  # Simula a escrita de texto em formato TXT
    yield file_path
    os.remove(file_path)

# Teste de leitura de arquivo PDF real
def test_read_pdf_file():
    file_path = "text_analyzer/test_files/curriulo_test_ramiro.pdf"  # Seu arquivo PDF real
    content = read_file(file_path)
    assert "Vaga para Desenvolvedor Python" in content
    assert "Django" in content
    assert "Flask" in content

# Teste de leitura de arquivo PDF temporário (usando a fixture)
def test_read_temp_pdf_file(temp_pdf_file):
    content = read_file(temp_pdf_file)
    assert "Vaga para Desenvolvedor Python" in content
    assert "Django" in content
    assert "Flask" in content

# Teste de leitura de arquivo TXT temporário (usando a fixture)
def test_read_temp_txt_file(temp_txt_file):
    content = read_file(temp_txt_file)
    assert "Vaga para Desenvolvedor Python" in content
    assert "Django" in content
    assert "Flask" in content

# Teste de erro - arquivo não encontrado
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_file("arquivo_inexistente.txt")

# Teste de erro - formato não suportado
def test_unsupported_file_format():
    with pytest.raises(ValueError):
        read_file("documento.zip")  # Arquivo com formato não suportado

# Teste de erro - arquivo vazio
def test_empty_file(temp_txt_file):
    with open(temp_txt_file, "w", encoding="utf-8") as f:
        f.write("")  # Escreve um arquivo vazio
    with pytest.raises(ValueError):
        read_file(temp_txt_file)

# Teste de erro - parâmetro incorreto
def test_invalid_file_type():
    with pytest.raises(TypeError):
        read_file(123)  # Parâmetro inválido (não é str nem TextIO)

# Teste de erro - erro ao abrir ou ler o arquivo (Simulando falha de IO)
@patch("builtins.open", side_effect=IOError("Erro ao tentar abrir o arquivo"))
def test_io_error(mock_open, temp_txt_file):
    with pytest.raises(IOError):
        read_file(temp_txt_file)

    # Simulando erro ao tentar ler o arquivo PDF
    with pytest.raises(IOError):
        read_file("temp_vaga_python.pdf")  # Tentando ler um arquivo que causará erro de IO
