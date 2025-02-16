import pytest
from text_analyzer.core.analyzer import TextAnalyzer
from text_analyzer.utils.file_handler import read_file
from text_analyzer.utils.text_cleaner import clean_text  # Importando a função de limpeza

def test_analyze_file(tmp_path):
    # Criando o arquivo de teste com conteúdo
    test_file = tmp_path / "documento.txt"
    test_file.write_text("Python é poderoso. Python é simples. Python é incrível!")

    analyzer = TextAnalyzer()
    text = read_file(str(test_file))

    # Limpando o texto antes de passar para o analisador
    cleaned_text = ' '.join(clean_text(text))

    analyzer.load_text(cleaned_text)  # Passa o texto limpo para o analisador

    # Testando frequência de palavras
    assert analyzer.word_frequencies["python"] == 3
    assert analyzer.word_frequencies["poderoso"] == 1
    assert analyzer.word_frequencies["simples"] == 1
    assert analyzer.word_frequencies["incrível"] == 1

    # Testando o comportamento com arquivo vazio
    empty_file = tmp_path / "vazio.txt"
    empty_file.write_text("")
    try:
        text_empty = read_file(str(empty_file))
        cleaned_text_empty = ' '.join(clean_text(text_empty))
        analyzer.load_text(cleaned_text_empty)
        assert analyzer.word_frequencies == {}
    except ValueError:
        # Espera-se que o arquivo vazio gere um ValueError
        pass

    # Testando com palavras maiúsculas e pontuação
    mixed_case_file = tmp_path / "maiusculas_pontuacao.txt"
    mixed_case_file.write_text("Python, python, PYTHON!")
    text_mixed_case = read_file(str(mixed_case_file))
    cleaned_text_mixed_case = ' '.join(clean_text(text_mixed_case))
    analyzer.load_text(cleaned_text_mixed_case)
    assert analyzer.word_frequencies["python"] == 3

