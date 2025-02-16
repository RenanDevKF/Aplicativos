import pytest
from text_analyzer.core.analyzer import TextAnalyzer
from text_analyzer.utils.file_handler import read_file

def test_analyze_file(tmp_path):
    # Criando o arquivo de teste com conteúdo
    test_file = tmp_path / "documento.txt"
    test_file.write_text("Python é poderoso. Python é simples. Python é incrível!")

    analyzer = TextAnalyzer()
    text = read_file(str(test_file))
    analyzer.load_text(text)

    # Testando frequência de palavras
    assert analyzer.word_frequencies["python"] == 3
    assert analyzer.word_frequencies["é"] == 3
    assert analyzer.word_frequencies["poderoso"] == 1
    assert analyzer.word_frequencies["simples"] == 1
    assert analyzer.word_frequencies["incrível"] == 1

    # Testando análise de frases
    assert len(analyzer.sentences) == 3

    # Testando o comportamento com arquivo vazio
    empty_file = tmp_path / "vazio.txt"
    empty_file.write_text("")
    text_empty = read_file(str(empty_file))
    analyzer.load_text(text_empty)
    assert analyzer.word_frequencies == {}

    # Testando com palavras maiúsculas e pontuação
    mixed_case_file = tmp_path / "maiusculas_pontuacao.txt"
    mixed_case_file.write_text("Python, python, PYTHON!")
    text_mixed_case = read_file(str(mixed_case_file))
    analyzer.load_text(text_mixed_case)
    assert analyzer.word_frequencies["python"] == 3
